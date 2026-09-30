# Source health and acquisition (2026-09-30)

Baseline: `python main.py inspect sources` on a read-only copy of the daemon database
(`data/eval/inventory-2026-09-30.db`, items 2026-09-25 09:33 .. 2026-09-30 09:21 UTC, 5.0 days) with
the daemon log. Every candidate feed below was fetched live from its official URL with the
collector's own User-Agent on 2026-09-30; "newest" is the newest entry date in the feed, not the
first entry (some feeds list oldest first). No access restriction was worked around.

## 1. Source health (before this change)

47 identities, 161 endpoints, 105 enabled, 49 observed, 52 enabled with no observation.

| Endpoint | Finding | Class | Action |
|---|---|---|---|
| `build_collectors()` | `import os` inside the govint `try`: a failed govint import raised UnboundLocalError at the later `os.environ` checks | code defect | fixed (module import) |
| RIPE Atlas item text | unparenthesised conditionals dropped target/name/probe lines when RTTs existed | code defect | fixed |
| Finance bridge VIX | `>25` tested first, so HIGH/EXTREME were unreachable | code defect | fixed |
| OFAC SDN (40 runs, 0 entries) | sdn.xml has a default namespace; `.//sdnEntry` matched 0 of 19,444 entries | parser bug | fixed (`{*}` paths, `is not None`) |
| GDELT (0) | DOC API answers "Queries containing OR'd terms must be surrounded by ()"; the Context API resets the connection | parser/query bug + provider | query fixed; 20 items per run now |
| Federal Register (0) | type names (`rules`) instead of API codes (`RULE`) -> count 0 | parser/query bug | fixed; stored as "Federal Register" |
| CRS (0) | congress.gov Cloudflare challenge (403) | access issue | kept enabled; now reported as an error; stored as "Congressional Research Service" |
| Defense.gov (264 runs, 0) | `/news/feed/` answers 403 Access Denied (Akamai) to feed clients | access issue | repointed to the official ArticleCS releases feed (works) |
| State Department (0) | `/rss/press-releases/` redirects to a PNG | bad endpoint | repointed to `/rss-feed/press-releases/feed/` (works) |
| Reuters World (0) | 404; Reuters has no public feed | bad endpoint / licensed | disabled with `access` note |
| Lawfare (0) | Cloudflare challenge (403) | access issue | kept enabled; RSS collector now logs `[err] ... 403` instead of `[ok] 0 items` |
| CSIS | feed answers, newest entry 2016; no current feed found at csis.org | bad endpoint (stale) | kept, marked stale in config |
| 9 Nitter accounts (264/264 errors) | nitter.poast.org no longer resolves; nitter.net refuses connections | provider issue | unchanged (recurrent errors visible) |
| IAEA (0) | feed healthy (15 entries); the collector keeps only safeguards/verification items | working as designed (sparse) | none |
| Wikipedia (15 pages, 0), SEC (7, 0), Currency (0), UX=F | emit only on edit surges / 8-K filings / threshold moves | event-driven | none |
| BGP 7 ASNs, cables AE/OM/SA, 3 DNS domains, OFAC 40 of 50 | templated records of one collector score >= 0.85 cosine to each other ("BGP status: AS12880 ... normal" vs AS58224: 0.884), so semantic dedup drops all but the first | pipeline dedup swallows templated structured records | diagnosed, not changed (dedup semantics) |
| OONI incidents | incident items link to `explorer.ooni.org/`, so the inventory cannot attribute them per endpoint | observability | noted |
| Config loaders | sources/entities/alerts/development_types YAML opened with the platform encoding (cp1252) -> "El País" read as "El PaÃ­s" | code defect (exposed by non-ASCII names) | fixed (`encoding="utf-8"`; previous files had non-ASCII only in comments) |

## 2. Acquisition matrix

Role = provenance source role (config/provenance.yaml): **primary** = authoritative for what the
institution itself did or said; **wire / independent** = counts toward independent corroboration;
**analysis** = commentary, never occurrence evidence. Status: live check on 2026-09-30.

| Source | Country/region | Lang | Class | Role | Feed / API | Auth | Access / licensing | Cadence (newest) | Corroboration role | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Associated Press | US / global | en | agency | wire | AP Media API | licence | apnews.com has no official feed; Cloudflare 403 | - | independent origin | high | **rejected: licensed only** |
| Reuters | UK / global | en | agency | wire | Reuters Connect | licence | public RSS discontinued (404) | - | independent origin | high | configured, **disabled** |
| AFP | FR / global | en/es | agency | wire | AFP API | licence | no public feed | - | independent origin | high | rejected: licensed only |
| EFE | ES / global | es | agency | wire | efe.com/feed | none | browser challenge 403; licensed content | - | independent origin | high | configured, **disabled** |
| ANSA | IT | it, en | agency | wire | ansa.it RSS (mondo, English) | none | public RSS, personal use | 30-09 (many/day) | independent origin; both feeds one origin | 1 | **added** |
| Europa Press | ES | es | agency | wire | europapress.es RSS internacional | none | public RSS | 30-09 | independent origin | 1 | **added** |
| Rai News | IT | it | public broadcaster | independent | rainews.it/rss/esteri | none | public RSS | 30-09 | independent origin | 1 | **added** |
| RTVE | ES | es | public broadcaster | independent | api2.rtve.es/rss | none | feeds answer but newest 2022 | stale | - | - | rejected: stale feeds |
| BBC Mundo | UK / LatAm | es | public broadcaster | independent | feeds.bbci.co.uk/mundo | none | public RSS | 30-09 | same origin as BBC World | 2 | **added (BBC endpoint)** |
| Deutsche Welle | DE | en (es available) | public broadcaster | independent | rss.dw.com | none | public RSS | 30-09 | independent origin | 2 | **added** |
| France 24 | FR | en, es | public broadcaster | independent | france24.com/{en,es}/rss | none | public RSS | 30-09 | both feeds one origin | 2 | **added** |
| NHK World | JP | ja | public broadcaster | independent | nhk.or.jp RSS | none | Japanese; English service not RSS | - | - | 3 | deferred: language |
| Il Sole 24 Ore | IT | it | newspaper | independent | ilsole24ore.com/rss/mondo | none | public RSS | 30-09 | independent origin | 1 | **added** |
| La Repubblica | IT | it | newspaper | independent | repubblica.it/rss/esteri | none | public RSS | 30-09 | independent origin | 2 | deferred: 3rd Italian outlet in batch 1 |
| Corriere della Sera | IT | it | newspaper | independent | xml2.corriereobjects.it | none | esteri feed newest 2025-03 | stale | - | - | rejected: stale feed |
| El País | ES | es | newspaper | independent | feeds.elpais.com internacional | none | public RSS | 30-09 | independent origin | 1 | **added** |
| El Mundo | ES | es | newspaper | independent | e00-elmundo.uecdn.es RSS | none | public RSS | 30-09 | independent origin | 2 | deferred: batch 2 |
| La Vanguardia | ES | es | newspaper | independent | lavanguardia.com/rss | none | public RSS | 30-09 | independent origin | 3 | deferred: batch 2 |
| ABC | ES | es | newspaper | independent | abc.es/rss | none | public RSS | 30-09 | independent origin | 3 | deferred: batch 2 |
| Clarín | AR | es | newspaper | independent | clarin.com/rss/mundo | none | public RSS | 29-09 | independent origin (LatAm) | 2 | **added** |
| Infobae | AR | es | newspaper | independent | infobae.com arc RSS | none | public RSS, high volume, mixed content | 30-09 | independent origin | 3 | deferred: signal-to-noise |
| El Tiempo | CO | es | newspaper | independent | eltiempo.com/rss/mundo | none | public RSS | 30-09 | independent origin | 3 | deferred |
| Kyiv Independent | UA | en | independent outlet | independent | kyivindependent.com RSS | none | public RSS | 30-09 | independent origin in a covered theatre | 2 | **added** |
| The Hindu / Times of India | IN | en | newspaper | independent | RSS | none | public RSS | 30-09 | independent origin | 3 | deferred: batch 2 (South Asia) |
| Al-Monitor | Middle East | en | specialist outlet | specialist | al-monitor.com/rss | none | public RSS; partly paywalled | 30-09 | specialist | 3 | deferred |
| ECB | EU | en | central bank | primary | ecb.europa.eu/rss/press.html | none | official | 30-09 | authoritative for ECB | 1 | **added** |
| Federal Reserve | US | en | central bank | primary | federalreserve.gov feeds (press, speeches) | none | official | 29-09 | authoritative for the Fed; one origin | 1 | **added** |
| Bank of England | UK | en | central bank | primary | bankofengland.co.uk/rss/news | none | official | 25-09 | authoritative for BoE | 2 | deferred: batch 2 |
| Bank of Japan | JP | en | central bank | primary | boj.or.jp/en/rss/whatsnew.xml | none | official; operational notices dominate | 30-09 | authoritative for BoJ | 3 | deferred: signal-to-noise |
| Swiss National Bank | CH | en | central bank | primary | snb.ch RSS | none | official | 24-09 | authoritative for SNB | 3 | deferred |
| BIS | intl | en | monetary institution | primary | bis.org/doclist/all_pressrels.rss | none | official | 23-09 | authoritative for BIS | 2 | **added** |
| IMF | intl | en | intl institution | primary | imf.org RSS | none | Akamai 403 | - | - | high | deferred: access blocked |
| World Bank | intl | en | intl institution | primary | search.worldbank.org API | none | RSS 404; API answers 401 for RSS format | - | - | 2 | deferred: needs API collector |
| OECD / UNCTAD | intl | en | intl institution | primary | RSS | none | Cloudflare 403 | - | - | 3 | deferred: access blocked |
| WTO | intl | en | intl institution | primary | wto.org latest news RSS | none | official | 29-09 | authoritative for WTO | 3 | deferred: batch 2 |
| United Nations | intl | en | intl institution | primary | news.un.org RSS; press.un.org RSS | none | official | 29-09 | authoritative for UN bodies; one origin | 1 | **added** |
| European Commission | EU | en | EU institution | primary | presscorner RSS | none | official | 30-09 | authoritative for the Commission | 1 | **added** |
| Council of the EU | EU | en | EU institution | primary | consilium.europa.eu RSS | none | official | 30-09 | authoritative for the Council | 1 | **added** |
| European Parliament | EU | en | EU institution | primary | europarl.europa.eu press RSS | none | official | 29-09 | authoritative for EP | 2 | **added** |
| EEAS | EU | en | EU institution | primary | - | none | no RSS found (listing pages only) | - | - | 2 | deferred: no feed |
| White House | US | en | US institution | primary | whitehouse.gov/news/feed | none | official | 29-09 | authoritative for the President | 1 | **added** |
| State Department | US | en | US institution | primary | state.gov/rss-feed/press-releases | none | official | 30-09 | authoritative | 1 | **repaired** |
| Department of Defense | US | en | US institution | primary | defense.gov ArticleCS releases RSS | none | official | 30-09 | authoritative | 1 | **repaired** |
| Treasury / OFAC | US | en | US institution | primary | ofac.treasury.gov/rss.xml; home.treasury.gov/rss.xml | none | OFAC RSS newest 2025-02; Treasury RSS a stale FAQ feed | stale | - | high | deferred: no current feed (SDN XML parser fixed) |
| Commerce BIS, USTR | US | en | US institution | primary | RSS | none | BIS 404; USTR RSS weekly digests only | - | - | 3 | deferred |
| SEC | US | en | US institution | primary | sec.gov/news/pressreleases.rss | none | official | 29-09 | enforcement only | 3 | deferred: low geopolitical value |
| Congress committees (HFAC, SFRC, HASC, SASC) | US | en | legislature | primary | committee RSS | none | HFAC stale (2025-03), HASC 404, Senate sites Akamai 403 | - | - | 2 | deferred: access / stale |
| Crisis Group | intl | en | think tank | analysis | crisisgroup.org/rss.xml | none | public RSS | 25-09 | commentary only | 1 | **added** |
| SIPRI | SE | en | think tank | analysis | sipri.org/rss/combined.xml | none | public RSS | 28-09 | commentary only | 2 | **added** |
| Bruegel | EU | en | think tank | analysis | bruegel.org/rss.xml | none | public RSS | 19-08 (sparse) | commentary only | 2 | **added** |
| MCC Brussels | EU | en (feed tagged hu) | think tank | analysis | brussels.mcc.hu/rss | none | public RSS | 31-07 (two months old) | commentary only | 3 | deferred: sparse; revisit |
| ECFR, IISS, Chatham House, ISW | EU/UK/US | en | think tank | analysis | RSS | none | 403 (bot protection) | - | - | 2 | deferred: access blocked |
| RUSI | UK | en | think tank | analysis | - | none | no feed found (404) | - | - | 3 | deferred: no feed |
| PIIE | US | en | think tank | analysis | piie.com RSS | none | feed dominated by future events | - | - | 3 | rejected: signal-to-noise |
| CSIS | US | en | think tank | analysis | csis.org/rss.xml (configured) | none | newest 2016 | stale | - | - | kept (stale, flagged) |

## 3. Canonical source identity

```
identity           the organisation              sources.yaml `identity` (default: feed name)
endpoint           one feed / query              a sources.yaml feed entry (collector + URL)
stored name        Source.name on items          the feed `name` (unchanged, historical rows untouched)
provenance origin  who originated the report     provenance.yaml `origin` = identity
```

Several feeds of one organisation share one identity and one origin, so they never count as
independent of each other: ANSA Mondo + ANSA English -> ANSA; BBC World + BBC Mundo -> BBC; Federal
Reserve Press + Speeches -> Federal Reserve; UN News + UN Press -> United Nations; France 24 +
France 24 Español -> France 24.

Existing inconsistencies:

| Stored name | Identity | Resolution |
|---|---|---|
| BBC World | BBC | identity declared; origin BBC already |
| Reuters World | Reuters | identity declared; feed disabled |
| Defense.gov | US Department of Defense | identity declared; origin already |
| State Department / Travel Advisories | US State Department | State Department declared; Travel Advisories is a separate collector, reported by `inspect sources`, not merged |
| government_documents | Federal Register / Congressional Research Service | split into one stored name per publisher (no stored rows existed under the old name) |
| USGS Seismic / Seismic Explosion Detector, RIPE NCC x3, Yahoo x2, OpenSky x4 | per provider | reported only; these are different collectors of one provider, not independent reports |
| @CENTCOM, @NATO, @bellingcat | provenance origins | reported: no declared identity (Nitter accounts are not in `rss_feeds`) |

Historical records are not rewritten.

## 4. Ranking and batches

Ranked by geopolitical value, independence, geographic and language diversity, access stability,
structured feed, licensing, signal-to-noise -- not by feed count.

**Batch 1 (implemented, 20 new identities):**
wire ANSA, Europa Press; public broadcasters Rai, DW, France 24 (+ BBC Mundo endpoint);
newspapers Il Sole 24 Ore, El País, Clarín, Kyiv Independent; primary ECB, Federal Reserve, BIS,
European Commission, Council of the EU, European Parliament, United Nations, White House;
analysis International Crisis Group, SIPRI, Bruegel. Repaired: DoD, State Department.
Disabled with reason: Reuters, EFE.

**Batch 2 (recommended next, all verified live):** La Repubblica, El Mundo, Bank of England, WTO,
The Hindu, DW Español, MCC Brussels (if its cadence resumes).

**Needs work before adding:** World Bank (API collector), IMF / OECD / UNCTAD / ECFR / IISS /
Chatham House / ISW / Senate committees (access blocked), EEAS and RUSI (no feed), Treasury/OFAC
recent actions (no current feed), AP / AFP / Reuters / EFE (licence).

## 5. Known limits exposed by the new sources

- The embedding model (all-MiniLM-L6-v2) and the NER model (en_core_web_sm) are English. Italian
  and Spanish reports cluster among themselves but not with English reports of the same
  Development (evaluation collection: FlyDubai story as one Italian and one English cluster), so
  corroboration across languages is undercounted. A multilingual embedding model would change
  clustering and is out of scope here.
- Semantic dedup drops templated structured records (above).
- Federal Register NOTICE documents are high-volume administrative notices; consider narrowing to
  PRESDOCU + RULE.
