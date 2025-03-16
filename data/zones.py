from mapgen.overlay.mastery_overlay import MasteryRegionMapOverlay
from mapgen.overlay.zone_overlay import ZoneMapOverlay

zone_ids: dict[str, list[int]] = {
    'city': [
        18,  # Divinity's Reach
        50,  # Lion's Arch
        91,  # The Grove
        139,  # Rata Sum
        218,  # Black Citadel
        326,  # Hoelbrak
    ],

    'lobby': [
        1155,  # Lion's Arch Aerodrome
        # 1483,  # Memory of Old Lion's Arch
    ],

    'outpost': [
        1370,  # Eye of the North
        1428,  # Arborstone
        1509,  # The Wizard's Tower
    ],

    'open_world': [
        15,  # Queensdale
        17,  # Harathi Hinterlands
        19,  # Plains of Ashford
        20,  # Blazeridge Steppes
        21,  # Fields of Ruin
        22,  # Fireheart Rise
        23,  # Kessex Hills
        24,  # Gendarran Fields
        25,  # Iron Marches
        26,  # Dredgehaunt Cliffs
        27,  # Lornar's Pass
        28,  # Wayfarer Foothills
        29,  # Timberline Falls
        30,  # Frostgorge Sound
        31,  # Snowden Drifts
        32,  # Diessa Plateau
        34,  # Caledon Forest
        35,  # Metrica Province
        39,  # Mount Maelstrom
        51,  # Straits of Devastation
        53,  # Sparkfly Fen
        54,  # Brisban Wildlands
        62,  # Cursed Shore
        65,  # Malchor's Leap
        73,  # Bloodtide Coast
        873,  # Southsun Cove
        988,  # Dry Top
        1015,  # The Silverwastes
        1041,  # Dragon's Stand
        1043,  # Auric Basin
        1045,  # Tangled Depths
        1052,  # Verdant Brink
        1165,  # Bloodstone Fen
        1175,  # Ember Bay
        1178,  # Bitterfrost Frontier
        1185,  # Lake Doric
        1195,  # Draconis Mons
        1203,  # Siren's Landing
        1210,  # Crystal Oasis
        1211,  # Desert Highlands
        1226,  # The Desolation
        1228,  # Elon Riverlands
        1248,  # Domain of Vabbi
        1263,  # Domain of Istan
        1271,  # Sandswept Isles
        1288,  # Domain of Kourna
        1301,  # Jahai Bluffs
        1310,  # Thunderhead Peaks
        1317,  # Dragonfall
        1330,  # Grothmar Valley
        1343,  # Bjora Marches
        1371,  # Drizzlewood Coast
        1422,  # Dragon's End
        1438,  # New Kaineng City
        1442,  # Seitung Province
        1452,  # The Echovald Wilds
        1490,  # Gyala Delve
        1510,  # Skywatch Archipelago
        1517,  # Amnytas
        1526,  # Inner Nayos
        1550,  # Lowland Shore
        1554,  # Janthir Syntri
    ],

    'festival': [
        922,  # Labyrinthine Cliffs
        929,  # The Crown Pavilion
    ],

    'homestead': [
        1558,  # Hearth's Glow
    ],

    'guild_hall': [
        1068,  # Gilded Hollow
        1069,  # Lost Precipice
        1214,  # Windswept Haven
        1419,  # Isle of Reflection
    ],

    'dungeon': [
        36,  # Ascalonian Catacombs
        76,  # Caudecus's Manor
        67,  # Twilight Arbor
        64,  # Sorrow's Embrace
        69,  # Citadel of Flame
        71,  # Honor of the Waves
        82,  # Crucible of Eternity
        112,  # The Ruined City of Arah
        872,  # Fractals of the Mists
    ],

    'raid': [
        1062,  # Spirit Vale
        1149,  # Salvation Pass
        1156,  # Stronghold of the Faithful
        1188,  # Bastion of the Penitent
        1264,  # Hall of Chains
        1303,  # Mythwright Gambit
        1323,  # The Key of Ahdashim
    ],

    'strike': [
        1352,  # Secret Lair of the Snowmen
        # 1331,  # Shiverpeaks Pass
        # 1351,  # Boneskinner
        # 1341,  # Fraenir of Jormag
        # 1344,  # Voice of the Fallen and Claw of the Fallen
        # 1357,  # Whisper of Jormag
        # 1362,  # Forging Steel
        # 1376,  # Cold War
        1432,  # Aetherblade Hideout
        1450,  # Xunlai Jade Junkyard
        1451,  # Kaineng Overlook
        1437,  # Harvest Temple
        1485,  # Old Lion's Court
        1515,  # Cosmic Observatory
        1520,  # Temple of Febe
    ],

    'story': [
        335,  # Claw Island
        1268,  # Fahranur, the First City
    ],

    'public_instance': [
        943,  # The Tower of Nightmares
        1412,  # Dragonstorm
        1482,  # The Battle for Lion's Arch
        1480,  # The Twisted Marionette
        1523,  # Convergences
    ],

    'lounge': [
        1465,  # Thousand Seas Pavilion
    ],

    'misc': [
        336,  # Chantry of Secrets
    ],
}

source_thresholds = {
    0: {'mastery_region': 'Central Tyria', 'access_req': 'gw2'},
    873: {'mastery_region': 'Central Tyria', 'access_req': 'lw1'},
    988: {'mastery_region': 'Central Tyria', 'access_req': 'lw2'},
    1032: {'mastery_region': 'Heart of Thorns', 'access_req': 'hot'},
    1165: {'mastery_region': 'Heart of Thorns', 'access_req': 'lw3'},
    1209: {'mastery_region': 'Path of Fire', 'access_req': 'pof'},
    1260: {'mastery_region': 'Path of Fire', 'access_req': 'lw4'},
    1329: {'mastery_region': 'Icebrood Saga', 'access_req': 'lw5'},
    1415: {'mastery_region': 'End of Dragons', 'access_req': 'eod'},
    1466: {'mastery_region': 'Central Tyria', 'access_req': 'lw1'},
    1488: {'mastery_region': 'End of Dragons', 'access_req': 'eod'},
    1501: {'mastery_region': 'Secrets of the Obscure', 'access_req': 'soto'},
    1541: {'mastery_region': 'Janthir Wilds', 'access_req': 'jw'},
}

"""
Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. This can also add custom data for the zones:
- label_rect: The continent rect bounds to display the zone label in. Useful if multiple labels would overlap.
- label_anchor: Two letter description for where in the zone or label rect we want to align the label. First letter is the horizontal alignment (l = left, m = middle, r = right),
second letter is vertical alignment (t = top, m = middle, b = bottom). Default is middle ('mm').
- label_size: Size multiplier for the labels.
- mastery_region: Mastery experience region, if it's different from the typical chronological map ID progression based on source_thresholds.
"""
all_zone_data_overrides: dict[int: dict] = {
    23: {  # Kessex Hills
        'label_rect': [[44448, 30464], [45856, 32512]]
    },
    335: {  # Claw Island
        'continent_rect': [[46720, 32256], [48000, 33792]]
    },
    336: {  # Chantry of Secrets
        'continent_rect': [[48896, 32576], [49664, 33280]]
    },
    872: {  # Fractals of the Mists
        'continent_id': 1,  # Fractals are technically in the Mists, but we might want to display them on the overworld map as well
        'continent_name': 'Tyria',
    },
    988: {  # Dry Top
        'continent_rect': [[36608, 32128], [38656, 33536]]
    },
    929: {  # The Crown Pavilion
        'label_rect': [[41146, 26880], [42970, 27648]],
        'label_anchor': 'rm',
    },
    943: {  # The Tower of Nightmares
        'name': "The Tower of Nightmares",
        'continent_rect': [[42852, 31020], [43940, 32172]],
        'label_rect': [[42628, 31116], [44164, 32076]]
    },
    1062: {  # Spirit Vale
        'continent_rect': [[36392, 28544], [37112, 30592]],
        'label_rect': [[36808, 28592], [39016, 29696]],
        'label_anchor': 'lt'
    },
    1069: {  # Lost Precipice
        'label_rect': [[32160, 29696], [34304, 30976]],
        'label_anchor': 'rm'
    },
    1149: {  # Salvation Pass
        'continent_rect': [[35582, 28544], [36392, 30338]],
        'label_rect': [[35710, 28592], [36264, 30306]],
        'label_anchor': 'mt'
    },
    1155: {  # Lion's Arch Aerodrome
        'access_req': 'gw2'
    },
    1156: {  # Stronghold of the Faithful
        'continent_rect': [[34729, 28544], [35582, 30338]],
        'label_rect': [[32052, 28592], [35166, 29696]],
        'label_anchor': 'rt'
    },
    1165: {  # Bloodstone Fen
        'label_size': 0.85,
    },
    1175: {  # Ember Bay
        'continent_rect': [[37374, 44676], [41214, 47358]]
    },
    1188: {  # Bastion of the Penitent
        'access_req': 'hot'
    },
    1195: {  # Draconis Mons
        'continent_rect': [[35228, 40290], [38176, 43134]]
    },
    1210: {  # Crystal Oasis
        'continent_rect': [[57256, 42304], [62376, 44800]]
    },
    1228: {  # Elon Riverlands
        'continent_rect': [[58240, 44800], [61824, 48192]]
    },
    1263: {  # Domain of Istan
        'continent_rect': [[55318, 59966], [58858, 63406]]
    },
    1264: {  # Hall of Chains
        'access_req': 'pof'
    },
    1288: {  # Domain of Kourna
        'continent_rect': [[63624, 59576], [67212, 63806]]
    },
    1303: {  # Mythwright Gambit
        'access_req': 'pof'
    },
    1323: {  # The Key of Ahdashim
        'access_req': 'pof'
    },
    1352: {  # Secret Lair of the Snowmen
        'name': "Strike Mission: Secret Lair of the Snowmen",
        'mastery_region': 'Central Tyria',
        'label_rect': [[51180, 24384], [53484, 25664]],
        'label_anchor': 'rm'
    },
    1370: {  # Eye of the North
        'continent_rect': [[57344, 21248], [58198, 22102]]
    },
    1419: {  # Isle of Reflection
        'continent_rect': [[21319, 103785], [23239, 105705]]
    },
    1428: {  # Arborstone
        'continent_rect': [[29185, 100890], [30141, 101657]]
    },
    1465: {  # Thousand Seas Pavilion
        'continent_rect': [[20900, 98253], [22052, 99405]],
        'label_rect': [[20644, 98253], [22308, 99405]],
        'label_size': 0.75,
        'access_req': 'gem'
    },
    1480: {  # The Twisted Marionette
        'continent_rect': [[51446, 32249], [52224, 33170]]
    },
}

"""Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. Similar to zone_data_overrides, but it includes additional changes for 
specific map overlays."""
conditional_zone_data_overrides: dict[type, dict[int: dict]] = {
    ZoneMapOverlay: {
        26: {  # Dredgehaunt Cliffs
            'label_rect': [[52672, 32524], [54080, 33664]],
        },
        27: {  # Lornar's Pass
            'label_rect': [[50720, 30112], [51968, 31548]],
            'label_anchor': 'mt',
        },
        36: {  # Ascalonian Catacombs
            'label_rect': [[61248, 29024], [62656, 30048]],
            'label_anchor': 'lb'
        },
        50: {  # Lion's Arch
            'label_rect': [[46976, 30800], [48704, 31636]],
            'label_anchor': 'rb'
        },
        64: {  # Sorrow's Embrace
            'label_rect': [[52704, 33792], [55232, 34816]],
            'label_anchor': 'lt'
        },
        67: {  # Twilight Arbor
            'label_rect': [[42560, 32672], [43968, 33728]],
            'label_anchor': 'lt'
        },
        69: {  # Citadel of Flame
            'label_rect': [[60032, 24064], [62080, 25344]],
            'label_anchor': 'lm'
        },
        71: {  # Honor of the Waves
            'label_rect': [[55424, 24448], [57344, 25600]],
            'label_anchor': 'lm'
        },
        73: {  # Bloodtide Coast
            'label_rect': [[48000, 33600], [50432, 35456]],
            'label_anchor': 'mt',
        },
        76: {  # Caudecus's Manor
            'label_rect': [[43984, 28144], [45818, 28800]],
            'label_anchor': 'rm'
        },
        82: {  # Crucible of Eternity+
            'label_rect': [[53952, 37728], [55328, 38592]],
            'label_anchor': 'lb'
        },
        139: {  # Rata Sum
            'continent_rect': [[37376, 36096], [39936, 38654]],
            'label_rect': [[37376, 37566], [39936, 38718]],
            'label_anchor': 'mt',
        },
        336: {  # Chantry of Secrets
            'label_rect': [[48448, 32576], [49203, 33280]],
            'label_size': 0.6,
            'label_anchor': 'rm',
        },
        872: {  # Fractals of the Mists
            'continent_rect': [[49392.2, 31889.7], [49392.2, 31889.7]],
            'label_rect': [[49632, 31644], [51753, 32252]],
            'label_anchor': 'lt',
            'label_size': 0.6
        },
        1043: {  # Auric Basin
            'label_rect': [[33408, 33984], [35200, 35328]],
            'label_anchor': 'mt',
        },
        1155: {  # Lion's Arch Aerodrome
            'continent_rect': [[49054, 31868], [49641, 32374]],
            'label_rect': [[47006, 31500], [49014, 32116]],
            'label_anchor': 'rb',
            'label_size': 0.6
        },
        1264: {  # Hall of Chains
            'continent_rect': [[51935.2, 32267.7], [51935.2, 32267.7]],
            'label_rect': [[52128, 31900], [54784, 32438]],
            'label_anchor': 'lb',
            'label_size': 0.7
        },
        1268: {  # Fahranur, the First City
            'label_rect': [[52048, 61488], [53904, 62768]],
            'label_size': 0.8
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[49331.4, 32136.9], [49331.4, 32136.9]],
            'label_rect': [[47006, 32084], [49014, 32630]],
            'label_anchor': 'rt',
            'label_size': 0.6
        },
        1370: {  # Eye of the North
            'label_rect': [[54944, 21248], [57248, 22102]],
            'label_anchor': 'rm',
            'access_req': 'gw2'
        },
        1371: {  # Drizzlewood Coast
            'label_rect': [[50128, 17809], [52304, 22289]]
        },
        1412: {  # Dragonstorm
            'label_rect': [[51776, 26112], [53696, 27648]]
        },
        1428: {  # Arborstone
            'label_rect': [[26817, 100890], [29121, 101657]],
            'label_anchor': 'rm'
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[50678, 32646], [51835, 33170]],
            'label_size': 0.7,
            'label_anchor': 'rt'
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The\u00A0Battle\u00A0for\nLion's\u00A0Arch",
            'continent_rect': [[48064, 30784], [50368, 32192]],
            'label_rect': [[49081, 30240], [50625, 30992]],
            'label_anchor': 'lb',
            'label_size': 0.6
        },
        1509: {  # The Wizard's Tower
            'label_rect': [[24839, 21882], [28071, 22682]],
            'label_anchor': 'lm',
        },
        1523: {  # Convergences
            'name': "Convergences",
            'continent_rect': [[24108, 22416], [24108, 22416]],
            'label_rect': [[21804, 22032], [23900, 22720]],
            'label_anchor': 'rt',
            'label_size': 0.8
        },
    },
    MasteryRegionMapOverlay: {
        26: {  # Dredgehaunt Cliffs
            'label_rect': [[52224, 32892], [54528, 33792]],
        },
        27: {  # Lornar's Pass
            'label_rect': [[50944, 30816], [51712, 31676]]
        },
        39: {  # Mount Maelstrom
            'label_rect': [[50688, 37760], [53056, 40192]],
        },
        50: {  # Lion's Arch
            'label_rect': [[48256, 30912], [50432, 32128]]
        },
        76: {  # Caudecus's Manor
            'label_rect': [[45056, 27776], [46336, 28800]]
        },
        335: {  # Claw Island
            'continent_rect': [[46720, 32512], [48000, 33792]],
            'label_size': 0.8
        },
        872: {  # Fractals of the Mists
            'continent_rect': [[46336, 31008], [48128, 31680]],
            'label_size': 0.75
        },
        1185: {  # Lake Doric,
            'label_size': 0.9
        },
        1264: {  # Hall of Chains
            'continent_rect': [[51840, 31996], [53760, 32764]]
        },
        1268: {  # Fahranur, the First City
            'label_size': 0.8
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[46336, 31680], [48128, 32352]],
            'label_size': 0.75,
        },
        1370: {  # Eye of the North
            'label_rect': [[57088, 21248], [58454, 22102]],
            'mastery_region': 'Central Tyria'
        },
        1428: {  # Arborstone
            'label_rect': [[28929, 100890], [30397, 101657]]
        },
        1432: {  # Strike Mission: Aetherblade Hideout
            'name': "Strike Mission:\nAetherblade Hideout",
            'continent_rect': [[23367, 103145], [25543, 104105]],
            'label_rect': [[23367, 103209], [25543, 104105]],
        },
        1437: {  # Strike Mission: Harvest Temple
            'name': "Strike Mission:\nHarvest Temple",
            'continent_rect': [[33382, 105550], [35046, 106510]],
            'label_rect': [[33382, 105614], [35046, 106510]],
        },
        1450: {  # Strike Mission: Xunlai Jade Junkyard
            'name': "Strike Mission:\nXunlai Jade Junkyard",
            'continent_rect': [[30049, 99930], [32161, 100890]],
            'label_rect': [[30217, 99994], [31993, 100890]],
        },
        1451: {  # Strike Mission: Kaineng Overlook
            'name': "Strike Mission:\nKaineng Overlook",
            'continent_rect': [[25928, 100660], [27912, 101620]],
            'label_rect': [[25992, 100724], [27848, 101620]],
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[50646, 32249], [51776, 33170]],
            'label_anchor': 'rm',
            'label_size': 0.75
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The Battle for Lion's Arch",
            'continent_rect': [[47584, 30288], [50592, 30928]],
            'label_rect': [[47584, 30352], [50592, 30928]],
            'label_size': 0.75
        },
        1485: {  # Strike Mission: Old Lion's Court
            'name': "Strike Mission:\nOld Lion's Court",
            'continent_rect': [[48288, 32128], [50144, 33088]],
            'label_rect': [[48608, 32192], [49824, 33088]],
        },
        1509: {  # The Wizard's Tower
            'label_rect': [[23271, 21882], [24935, 22650]],
            'label_size': 0.9
        },
        1515: {  # Strike Mission: Cosmic Observatory
            'name': "Strike Mission:\nCosmic Observatory",
            'continent_rect': [[27302, 22650], [29482, 23674]],
            'label_rect': [[27444, 22650], [29340, 23674]],
        },
        1520: {  # Strike Mission: Temple of Febe
            'name': "Strike Mission:\nTemple of Febe",
            'continent_rect': [[19691, 24076], [21871, 25100]],
            'label_rect': [[19865, 24076], [21697, 25100]],
        },
        1523: {  # Convergences
            'name': "Convergences",
            'continent_rect': [[19691, 21004], [21871, 21900]],
            'label_rect': [[19691, 21004], [21871, 21900]],
            'label_size': 0.75
        },
    }
}

"""Map IDs to ignore for specific map overlays."""
conditional_zone_blacklist: dict[type, list[int]] = {
    ZoneMapOverlay: [
        1352,  # Secret Lair of the Snowmen
        1432,  # Aetherblade Hideout
        1450,  # Xunlai Jade Junkyard
        1451,  # Kaineng Overlook
        1437,  # Harvest Temple
        1485,  # Old Lion's Court
        1515,  # Cosmic Observatory
        1520,  # Temple of Febe
    ],
    MasteryRegionMapOverlay: [
        336,  # Chantry of Secrets
        1155,  # Lion's Arch Aerodrome
    ]
}

conditional_custom_zones: dict[type, list[dict]] = {
    MasteryRegionMapOverlay: [
        {
            'name': '\n'.join([
                "Strike Missions:",
                "   Shiverpeaks Pass",
                "   Fraenir of Jormag",
                "   Voice of the Fallen",
                "      and Claw of the Fallen",
                "   Boneskinner",
                "   Whisper of Jormag",
                "   Forging Steel",
                "   Cold War",
            ]),
            'category': 'strike',
            'continent_rect': [[59222, 20384], [62614, 23232]],
            'label_rect': [[59350, 20384], [62998, 23232]],
            'label_anchor': 'lm',
            'mastery_region': 'Icebrood Saga',
            'access_req': 'lw5',
        },
        {
            'name': "Dragon Response Missions",
            'category': 'misc',
            'continent_rect': [[55382, 20288], [58838, 21056]],
            'mastery_region': 'Icebrood Saga',
            'access_req': 'lw5',
        },
    ],
}
