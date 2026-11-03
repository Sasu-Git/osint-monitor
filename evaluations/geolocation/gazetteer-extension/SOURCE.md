# Location-layer gazetteer extension: source

| Item | Value |
|---|---|
| Source | GeoNames, https://download.geonames.org/export/dump/ (CC BY 4.0, geonames.org) |
| Files | `cities15000.zip` (all populated places with population ≥ 15,000), `countryInfo.txt` |
| Downloaded | 2026-11-03T08:15:56Z, once; raw files kept outside the repo (`C:\Users\EugenioVardiero\geonames-raw\`) |
| `cities15000.zip` sha256 | `f3bce12026e673fbef0833cd7fe1960009c90576a45ac208e73544e16d5bfbc5` |
| `cities15000.txt` sha256 (unzipped) | `070b655e0f3fc758cd1caedf5f2989d9b37b02ee284e3634d9cc14d7ee35e3c2` |
| `countryInfo.txt` sha256 | `79f8f59ea01cbb40438bf1856dd6c2ff201f03f8fc72d0530b2646aaf603ef04` |
| Build script | `build_extension.py` (sha256 `432954ee1b927b1c156bfd131007ec87a0981f8d72ba5933a018ad59aefcc017`) |
| Derived file | `osint_monitor/processors/data/place_extension.json` (sha256 `5924ddf2668243aa19ec570d07d6fdb1121010c7a0db1523c1021a98c600ba12`, 7.5 MB); rebuilt twice, identical bytes |

**Build output:**
- 34,082 places kept; 115 dropped because their country is not in the gazetteer (small territories: Aruba,
  Bermuda, Faroe Islands, Gibraltar, …).
- 147,524 names; 2,539 of them have candidates in more than one country.

**Why this source:** it is an independent bulk dataset, and nothing in it was chosen from the evaluation cases. It
replaces the live country-restricted geocoder (Nominatim) that L2 assumes, per the owner's 2026-11-03 instruction.
