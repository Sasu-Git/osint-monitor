"""Headlines of real clusters from the 2026-09-24 live run that exposed wrong
situation joins and cluster over-merges. Kept verbatim as regression fixtures."""

# Event #5: grouped into US-Iran because the cluster mentioned Iran; it is a US-China summit.
TRUMP_XI_SUMMIT = [
    ("Trump orders all US agencies to refer to AI as 'super intelligence'",
     "President Donald Trump said all United States documents will use the term 'super'."),
    ("Trump-Xi summit live: Trade, AI, Iran and Taiwan top US-China talks",
     "Xi's first White House visit in more than a decade comes amid ongoing disputes over trade, AI, Taiwan and war in Iran."),
    ("Trump and Xi come face-to-face as US and China battle to win the AI race",
     "The US and China are vying for AI supremacy while seeking to keep it under human control."),
    ("Xi begins first full day of US visit to meet Trump with White House ceremony", ""),
    ("Chinese CEOs fly to US on own, await invites to Trump's state dinner for Xi Jinping",
     "A small group of Chinese CEOs holding US visas has arrived in Washington."),
    ("China's overseas investment hits record US$214 billion. Why are US-bound flows plunging?", ""),
    ("Red carpet vs empty tarmac: Xi's US welcome fuels debate over Takaichi's no-show reception", ""),
    ("Xi-Trump summit day 1 highlights: red carpet for China's leader, Rubio defends visit, and more", ""),
    ("US tenor Christopher Macchio booked for Xi-Trump state dinner performance", ""),
    ("First lady Peng Liyuan's English takes the spotlight in exchange with Melania Trump", ""),
    ("Beyond the Rose Garden and the military review, Trump and Xi get down to business",
     "Chinese President Xi Jinping and US President Donald Trump got down to business on Thursday."),
]

# Event #1: grouped into Russia-Ukraine; five unrelated defense stories.
NAVY_CYBER = [
    ("Navy wants more offensive, 'expeditionary' cyber capabilities",
     "What I would offer to industry, if you are interested in talking about expeditionary cyber, please come talk to me."),
    ("The still-formidable F-16 will be even more capable with better electronic warfare",
     "A Viper modernization that includes EW, radar, EO/IR, and navigation."),
    ("The future of European airpower might be unmanned",
     "With one sixth-gen fighter program in Europe dead, could the future for European airpower be drones?"),
    ("Report: CIA warned Europe of Russian drone attack from vessels in the Mediterranean",
     "The CIA has warned European countries of a suspected Russian plot to launch drones from commercial vessels."),
    ("Winning by the Rules: Optimizing Weapons Reviews in the Age of Technological Innovation",
     "We spare the reader another detailed story from Ukraine."),
]

# Event #3: grouped into US-Iran; a Syria story merged with Gulf and ADS-B items.
SYRIA_BASES = [
    ("Syria looks to end foreign military presence, have sovereignty over all bases: President",
     "Damascus very soon will not have the necessity to have any foreign military presence."),
    ("US Navy destroyers tested in Middle East as demands mount",
     "Navy destroyers are concentrated in the Middle East as U.S. forces conduct operations against Iran."),
    ("Gulf nations keep oil flowing amid Iran war, but it's getting costly",
     "When Iran shut down the Strait of Hormuz at the start of the war, many feared that prices would skyrocket."),
    ("Military aircraft snapshot: 431 globally | persian_gulf: 2, eastern_med: 3, western_europe: 62", ""),
    ("TANKER ACTIVITY: 1 tanker(s) over Persian Gulf / Iran Theater — active refueling operations", ""),
]

US_IRAN_TALKS = [
    ("US and Iran resume nuclear talks in Muscat",
     "The United States and Iran resumed indirect nuclear talks in Muscat on Tuesday."),
    ("Iran's foreign minister meets US envoy in Oman for nuclear talks", ""),
    ("Iranian and US negotiators meet in Muscat for nuclear talks", ""),
]

RUSSIA_UKRAINE_STRIKES = [
    ("Russian drones strike Kyiv energy infrastructure overnight",
     "Russia launched a wave of drones at Kyiv overnight, Ukraine's air force said."),
    ("Russia hits Kyiv power grid in overnight drone attack", ""),
    ("Ukraine says Russian drone attack on Kyiv damaged energy sites", ""),
]

# 2026-09-24 eval run, event #1: principals came out as {AI, China}; Trump fell below support
# because outlets named him in different grammatical forms ("Trump-Xi", "Trump’s", "Xi-Trump").
TRUMP_XI_SUMMIT_SMALL = [
    ("Trump-Xi summit live: Trade, AI, Iran and Taiwan top US-China talks",
     "Xi’s first White House visit in more than a decade comes amid ongoing disputes over trade, AI, Taiwan and war in Iran."),
    ("Xi-Trump summit day 1 highlights: red carpet for China’s leader, Rubio defends visit, and more",
     "We have put together stories from our coverage of Xi and Trump’s meeting in the US so far"),
    ("Chinese CEOs fly to US on own, await invites to Trump’s state dinner for Xi Jinping",
     "A small group of Chinese CEOs holding US visas has arrived in Washington after travelling separately "
     "from President Xi Jinping’s official entourage, according to multiple sources familiar with the mat"),
    ("Trump and Xi come face-to-face as US and China battle to win the AI race",
     "The US and China are vying for AI supremacy while seeking to keep it under human control."),
]

# event #3: "Aussie" and "Australian" came out as two separate actors
F35_PARTS = [
    ("Has China received US F-35 parts by diverting an Australian shipment?",
     "Australia and US investigate F-35 parts mistakenly sent to Hong Kong amid concerns over sensitive military technology."),
    ("Aussie defense chief confirms missing F-35 parts, says none are ‘sensitive’",
     "After parts reportedly made their way to Hong Kong, a Lockheed Martin spokesperson told Breaking Defense "
     "that the missing components “are unserviceable and deemed low risk for exploitation.&#8221;"),
]

# event #5: "Air Force’s" kept its possessive as a separate actor
AIR_FORCE_CASI = [
    ("Fate of Air Force’s China Aerospace Studies Institute up in air",
     "The China Aerospace Studies Institute will carry on by “leveraging assigned military service members "
     "to accomplish its objectives,” according to an Air Force spokesperson."),
    ("Air Force, civilian staff dispute status of China Aerospace Studies Institute", "On Oct"),
    ("The Air Force says its China think-tank will continue. It’s director says it’s basically dead.",
     "The Air Force’s stance that the China Aerospace Studies Institute can function without civilian staff "
     "is “not credible,” its Brendan Mulvaney told Breaking Defense."),
]

# 2026-09-24 eval run, event #7: 18 unrelated quakes from two seismic feeds in one event
# because their templated text embeds alike. (source, source type, external_id, url, title, content, published)
SEISMIC_RECORDS = [
    ("USGS Seismic", "structured_api", "usgs_us6000txbm", "https://earthquake.usgs.gov/earthquakes/eventpage/us6000txbm",
     "Earthquake M5.2 - 139 km SW of Kokopo, Papua New Guinea",
     "Magnitude: 5.2 | Depth: 95.6 km (deep) | Location: -5.3396,151.4915 | Place: 139 km SW of Kokopo, Papua New Guinea",
     "2026-09-24 12:29:58"),
    ("Seismic Explosion Detector", "infrastructure", "seis_exp_ci41338455", "https://earthquake.usgs.gov/earthquakes/eventpage/ci41338455",
     "Shallow seismic: M1.63 depth=-1km at 13 km NE of Big Bear City, CA — explosion likelihood: HIGH",
     "Magnitude: 1.63\nDepth: -1 km\nLocation: 34.3298333333333, -116.7305\nPlace: 13 km NE of Big Bear City, CA\n"
     "Explosion likelihood: HIGH (score: 0.60)\n", "2026-09-24 12:54:08"),
    ("USGS Seismic", "structured_api", "usgs_us6000tx29", "https://earthquake.usgs.gov/earthquakes/eventpage/us6000tx29",
     "Earthquake M5.3 - 51 km WSW of Arauco, Argentina",
     "Magnitude: 5.3 | Depth: 121.5 km (deep) | Location: -28.7298,-67.2912 | Place: 51 km WSW of Arauco, Argentina",
     "2026-09-23 09:21:14"),
    ("Seismic Explosion Detector", "infrastructure", "seis_exp_nn00924831", "https://earthquake.usgs.gov/earthquakes/eventpage/nn00924831",
     "Shallow seismic: M1.82 depth=3.9895km at 20 km ESE of Silver Springs, Nevada — explosion likelihood: MODERATE",
     "Magnitude: 1.82\nDepth: 3.9895 km\nLocation: 39.3388, -119.0131\nPlace: 20 km ESE of Silver Springs, Nevada\n"
     "Explosion likelihood: MODERATE (score: 0.45)\n", "2026-09-24 04:11:57"),
    ("Seismic Explosion Detector", "infrastructure", "seis_exp_nc75440792", "https://earthquake.usgs.gov/earthquakes/eventpage/nc75440792",
     "Shallow seismic: M1.52 depth=0.680000007152557km at 15 km WSW of Firebaugh, CA — explosion likelihood: HIGH",
     "Magnitude: 1.52\nDepth: 0.680000007152557 km\nLocation: 36.8261680603027, -120.613998413086\n"
     "Place: 15 km WSW of Firebaugh, CA\nExplosion likelihood: HIGH (score: 0.60)\n", "2026-09-24 11:21:24"),
    ("USGS Seismic", "structured_api", "usgs_usauto6000tx3m,us6000tx3m", "https://earthquake.usgs.gov/earthquakes/eventpage/us6000tx3m",
     "Earthquake M5.7 - 180 km NW of Hihifo, Tonga",
     "Magnitude: 5.7 | Depth: 10.0 km (deep) | Location: -14.9369,-175.1114 | Place: 180 km NW of Hihifo, Tonga",
     "2026-09-23 14:41:02"),
]

# event #8: ADS-B snapshots and a flight-route reading merged into a "development"
ADSB_RECORDS = [
    ("ADSB Military Tracks", "adsb", "adsb_snapshot_202609241549", "https://api.adsb.lol/v2/mil",
     "Military aircraft snapshot: 375 globally | persian_gulf: 4, eastern_med: 2, western_europe: 26",
     "Global military aircraft tracked: 375\nBy region: persian_gulf: 4, eastern_med: 2, western_europe: 26",
     "2026-09-24 15:49:14"),
    ("Flight Route Monitor", "infrastructure", "flight_eastern_med_2026092415", "https://opensky-network.org/",
     "FLIGHT AVOIDANCE: Eastern Mediterranean / Lebanon-Syria — only 16 commercial flights (normal: 20+)",
     "Zone: Eastern Mediterranean / Lebanon-Syria\nTotal aircraft: 16\nCommercial: 16 (normal floor: 20)\nMilitary: 0",
     "2026-09-24 15:55:44"),
    ("ADSB Military Tracks", "adsb", "adsb_force_concentration_202609241549", "https://globe.adsbexchange.com/",
     "MILITARY CONCENTRATION: 26 aircraft over Western Europe (bomber staging)",
     "Breakdown: 14 other_military, 8 cargo, 3 isr_recon, 1 tanker\nRegion: RAF Fairford (B-1B/B-52 base), bomber departure routes",
     "2026-09-24 15:49:14"),
    ("ADSB Military Tracks", "adsb", "adsb_force_concentration_202609241602", "https://globe.adsbexchange.com/",
     "MILITARY CONCENTRATION: 5 aircraft over Persian Gulf / Iran Theater",
     "Breakdown: 2 cargo, 2 other_military, 1 tanker\nRegion: Operation Epic Fury theater, Hormuz, Iranian airspace",
     "2026-09-24 16:02:11"),
]
