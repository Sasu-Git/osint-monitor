"""Trend anomaly baseline (post-soak item 2): stable source cohort, event time, outage days skipped, rebuilt from items.
A change in the source set or a collection backlog must not raise an anomaly by itself; a real surge must."""
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.analysis.trends import detect_anomalies
from osint_monitor.core.database import Base, Entity, ItemEntity, RawItem, Source

NOW = datetime(2026, 10, 13, 12)


@pytest.fixture
def s(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 't.db'}")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    engine.dispose()


class World:
    def __init__(self, s):
        self.s, self.n = s, 0
        self.entities = {}

    def source(self, name):
        src = Source(name=name, type="rss", url=f"https://{name}.invalid/")
        self.s.add(src)
        self.s.flush()
        return src.id

    def entity(self, name):
        if name not in self.entities:
            e = Entity(canonical_name=name, entity_type="GPE")
            self.s.add(e)
            self.s.flush()
            self.entities[name] = e.id
        return self.entities[name]

    def items(self, source_id, published, count, mentions=(), fetched=None):
        for _ in range(count):
            self.n += 1
            item = RawItem(source_id=source_id, title=f"item {self.n}", content_hash=f"h{self.n}",
                           published_at=published, fetched_at=fetched or published)
            self.s.add(item)
            self.s.flush()
            for m in mentions:
                self.s.add(ItemEntity(item_id=item.id, entity_id=self.entity(m)))
        self.s.flush()

    def steady(self, source_id, days, per_day=20, bogota=3, start=None):
        """``days`` days of history ending before the current 24 h window: per_day items, ``bogota`` mention it."""
        for d in range(days, 0, -1):
            t = NOW - timedelta(days=d, hours=1)
            if start and t < start:
                continue
            self.items(source_id, t, bogota, mentions=["Bogota"])
            self.items(source_id, t, per_day - bogota, mentions=["Other"])


def names(anomalies):
    return sorted(a.entity_name for a in anomalies)


def test_a_steady_series_raises_nothing(s):
    w = World(s)
    a = w.source("old")
    w.steady(a, 20)
    w.items(a, NOW - timedelta(hours=3), 3, ["Bogota"])
    assert detect_anomalies(s, NOW) == []


def test_a_real_surge_from_established_sources_is_an_anomaly(s):
    w = World(s)
    a = w.source("old")
    w.steady(a, 20)
    w.items(a, NOW - timedelta(hours=3), 15, ["Bogota"])
    found = detect_anomalies(s, NOW)
    assert names(found) == ["Bogota"] and found[0].sigma >= 2


def test_a_new_source_does_not_raise_an_anomaly_by_itself(s):
    w = World(s)
    a, b = w.source("old"), w.source("new")
    w.steady(a, 20)
    w.steady(b, 5, per_day=100, bogota=40)                  # joined 5 days ago, writes about Bogota a lot
    w.items(a, NOW - timedelta(hours=3), 3, ["Bogota"])
    w.items(b, NOW - timedelta(hours=3), 40, ["Bogota"])
    assert detect_anomalies(s, NOW) == []


def test_a_backlog_collected_at_once_counts_on_its_publication_days(s):
    w = World(s)
    a = w.source("old")
    w.steady(a, 20)
    for d in (3, 2):                                       # published during an outage, collected just now
        w.items(a, NOW - timedelta(days=d, hours=1), 3, ["Bogota"], fetched=NOW - timedelta(minutes=5))
    w.items(a, NOW - timedelta(hours=3), 3, ["Bogota"])
    assert detect_anomalies(s, NOW) == []


def test_outage_days_are_not_baseline_days(s, monkeypatch):
    import osint_monitor.analysis.trends as trends
    w = World(s)
    a = w.source("old")
    w.steady(a, 20)
    # an outage: on four days only one item was collected; as baseline days they would drag the mean down
    for d in (4, 5, 6, 7):
        for item in s.query(RawItem).filter(RawItem.published_at == NOW - timedelta(days=d, hours=1)).all()[1:]:
            s.query(ItemEntity).filter(ItemEntity.item_id == item.id).delete()
            s.delete(item)
    s.flush()
    w.items(a, NOW - timedelta(hours=3), 6, ["Bogota"])    # an ordinary day after the outage
    assert detect_anomalies(s, NOW) == []
    monkeypatch.setattr(trends, "INCOMPLETE_DAY_RATIO", 0.0)   # outage days kept: the mean drops, a false alarm
    assert names(detect_anomalies(s, NOW)) == ["Bogota"]


def test_too_little_cohort_history_raises_nothing(s):
    w = World(s)
    a = w.source("young")
    w.steady(a, 10)                                        # 10 days: not yet in the 14-day cohort
    w.items(a, NOW - timedelta(hours=3), 30, ["Bogota"])
    assert detect_anomalies(s, NOW) == []


def test_a_rare_entity_needs_at_least_five_mentions(s):
    w = World(s)
    a = w.source("old")
    w.steady(a, 20)
    w.items(a, NOW - timedelta(hours=3), 4, ["Waze"])      # never mentioned before: 4 is still noise
    assert detect_anomalies(s, NOW) == []
    w.items(a, NOW - timedelta(hours=2), 1, ["Waze"])
    assert names(detect_anomalies(s, NOW)) == ["Waze"]
