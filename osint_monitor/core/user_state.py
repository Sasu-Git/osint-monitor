"""Personal presentation preferences: which countries and topics the reader wants surfaced, quietened or hidden.

User state, not intelligence state. It lives in its own SQLite file (OSINT_USER_STATE_DB, default
data/user_state.db), never in the intelligence database, so it cannot change a Development, a Situation,
a confidence class or any evidence, and the pipeline never reads it.

    preferences(profile, scope, key, level, updated_at)   primary key (profile, scope, key)

- profile: "default" until there are user accounts.
- scope:   "country" (key = stable country id, ISO 3166-1 alpha-3 or Natural Earth code)
           "domain"  (key = an EventDomain value).
           Later scopes fit the same row: "situation" (follow / mute by Situation slug), "requirement",
           "last_seen". They are not implemented.
- level:   HIGH / LOW / MUTED. NORMAL is the absence of a row.
"""

from __future__ import annotations

import os
from datetime import datetime
from enum import Enum
from pathlib import Path

from sqlalchemy import DateTime, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DEFAULT_PROFILE = "default"
SCHEMA_VERSION = 1


class Level(str, Enum):
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"
    MUTED = "MUTED"


class Scope(str, Enum):
    COUNTRY = "country"
    DOMAIN = "domain"


class _Base(DeclarativeBase):
    pass


class Preference(_Base):
    __tablename__ = "preferences"

    profile: Mapped[str] = mapped_column(String(64), primary_key=True)
    scope: Mapped[str] = mapped_column(String(32), primary_key=True)
    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class UserStateMeta(_Base):
    __tablename__ = "user_state_meta"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)


def default_path() -> Path:
    env = os.environ.get("OSINT_USER_STATE_DB")
    if env:
        return Path(env)
    from osint_monitor.core.config import DATA_DIR
    return DATA_DIR / "user_state.db"


_factories: dict[str, sessionmaker] = {}


def _factory(path: Path | None = None) -> sessionmaker:
    path = Path(path or default_path())
    key = str(path.resolve())
    if key not in _factories:
        path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(f"sqlite:///{path}", connect_args={"timeout": 10})
        _Base.metadata.create_all(engine)
        make = sessionmaker(bind=engine)
        with make() as s:
            if s.get(UserStateMeta, "schema_version") is None:
                s.add(UserStateMeta(key="schema_version", value=str(SCHEMA_VERSION)))
                s.commit()
        _factories[key] = make
    return _factories[key]


class PriorityStore:
    """Read and write one profile's priorities. Keys are validated by the caller (stable ids only)."""

    def __init__(self, path: Path | None = None, profile: str = DEFAULT_PROFILE):
        self._make = _factory(path)
        self.profile = profile

    def levels(self, scope: Scope) -> dict[str, Level]:
        with self._make() as s:
            rows = s.scalars(select(Preference).where(Preference.profile == self.profile,
                                                      Preference.scope == scope.value))
            return {r.key: Level(r.level) for r in rows}

    def get(self, scope: Scope, key: str) -> Level:
        return self.levels(scope).get(key, Level.NORMAL)

    def set(self, scope: Scope, key: str, level: Level) -> None:
        with self._make() as s:
            row = s.get(Preference, (self.profile, scope.value, key))
            if level is Level.NORMAL:
                if row is not None:
                    s.delete(row)
            elif row is None:
                s.add(Preference(profile=self.profile, scope=scope.value, key=key, level=level.value,
                                 updated_at=datetime.utcnow()))
            else:
                row.level, row.updated_at = level.value, datetime.utcnow()
            s.commit()

    def reset(self, scope: Scope | None = None) -> None:
        with self._make() as s:
            q = s.query(Preference).filter(Preference.profile == self.profile)
            if scope is not None:
                q = q.filter(Preference.scope == scope.value)
            q.delete()
            s.commit()
