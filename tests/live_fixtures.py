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
