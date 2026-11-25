# stories.py — the world news of Tuesday 24 November 2026, as reported that
# day (Reuters / AP / BBC / Al Jazeera / Kyiv Independent / ISW / Daily
# Summary of World, 24 Nov 2026 editions).  Only events that happened, or
# were first reported, on 24 November 2026 are used here; nothing from
# earlier days is presented as the day's news.
#
# Layout contract with main.py:
#   LEAD — three big cards across the top of the poster.
#   MID  — four cards in a 2x2 grid below the lead row.
#   TICKER — one-line "also today" items along the bottom.

DATE_LINE = "TUESDAY 24 NOVEMBER 2026"
MASTHEAD = "THE WORLD IN ONE IMAGE"
SUBHEAD = "ONE DAY  •  ONE PICTURE  •  THE WORLD'S NEWS"

LEAD = [
    {
        "kicker": "UNITED STATES  •  VERDICT",
        "title": "HUAWEI GUILTY",
        "body": "A US jury convicts Huawei of stealing trade secrets and bank fraud on 10 of 12 counts, but acquits it of racketeering. Huawei says it will appeal.",
        "icon": "chip",
        "accent": (196, 58, 43),      # red
    },
    {
        "kicker": "STRAIT OF HORMUZ  •  SHIPPING",
        "title": "FOUR TANKERS HIT BY MINES",
        "body": "Iran says four tankers struck naval mines and caught fire in the Strait of Hormuz. The IRGC says it also attacked a container ship. Tehran orders the strait closed day by day.",
        "icon": "tanker",
        "accent": (212, 160, 23),     # gold
    },
    {
        "kicker": "UKRAINE  •  WAR AT SEA",
        "title": "KYIV STRIKES RUSSIAN SHIPS",
        "body": "Ukraine drones hit the cargo ship Sparta II in the Gulf of Finland and a Russian corvette off Libya. Poland cites a new airspace violation. Putin admits oil strikes strain Russia's fuel market.",
        "icon": "warship",
        "accent": (31, 122, 109),     # teal
    },
]

MID = [
    {
        "kicker": "SAUDI ARABIA  •  YEMEN WAR",
        "title": "HOUTHI STRIKE HITS RIYADH TOWER",
        "body": "A drone attack on the PIF tower in Riyadh's financial district wounds 11 people, the second hit in under a week. Yemen's army says Houthi fighters are 60 km from Aden.",
        "icon": "tower",
        "accent": (196, 58, 43),
    },
    {
        "kicker": "COLOMBIA  •  HOSTAGE CRISIS",
        "title": "25 HELD IN CARTAGENA SUPERMARKET",
        "body": "Armed men seize a supermarket in Cartagena and hold 25 people hostage. A car bomb outside offices in Villavicencio injures 23 on the eve of the FARC peace deal's 10th anniversary.",
        "icon": "shop",
        "accent": (212, 160, 23),
    },
    {
        "kicker": "GAZA  •  CEASEFIRE UNDER STRAIN",
        "title": "HAMAS SECURITY CHIEF KILLED",
        "body": "An Israeli strike kills Hamas internal security chief Naeem Abu Mohammed Nahel in Gaza despite the October ceasefire. Gaza declares a meningitis epidemic alert after cases surge eightfold.",
        "icon": "cross",
        "accent": (31, 122, 109),
    },
    {
        "kicker": "KOREA  •  NATO  •  SPACE",
        "title": "RUSSIAN JETS NEAR ULLEUNGDO",
        "body": "South Korea scrambles fighters and orders islanders to shelter as Russian aircraft approach Ulleungdo. NATO vows to defend against space threats after reports of a nuclear-armed Russian satellite.",
        "icon": "jets",
        "accent": (196, 58, 43),
    },
]

TICKER = [
    "ICJ RULING: 14 NATIONS BACK ROHINGYA GENOCIDE VERDICT AGAINST MYANMAR",
    "HASINA PLANS RETURN TO BANGLADESH ON 16 DECEMBER",
    "TURKISH HELICOPTER CRASH KILLS FIVE NEAR ESKISEHIR",
    "HANOI RESTAURANT BLAST KILLS AT LEAST SIX",
    "US BLACKLISTS MEGASPEED IN NVIDIA SPY SCANDAL",
    "EL CHAPO ISIDRO CAPTURED WITH US DRONE HELP; MEXICO TO TRY HIM",
    "ZELENSKY URGES FOUR-PARTY TALKS WITH RUSSIA, US AND EUROPE",
    "SENEGAL REGAIN AFRICA CUP OF NATIONS TITLE ON APPEAL",
    "UK SANCTIONS YEMEN'S HOUTHIS AND FOUR SENIOR OFFICIALS",
    "CHINA SENTENCES OFFICIAL TO DEATH FOR SPYING",
]

FOOTER = "SOURCES: REUTERS  •  AP  •  BBC  •  AL JAZEERA  •  KYIV INDEPENDENT  •  ISW  •  DAILY SUMMARY OF WORLD  —  24 NOV 2026"
