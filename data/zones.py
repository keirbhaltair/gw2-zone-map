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

    'hub': [
        1155,  # Lion's Arch Aerodrome
        1370,  # Eye of the North
        1428,  # Arborstone
        # 1483,  # Memory of Old Lion's Arch
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
        1574,  # Bava Nisos
        1575,  # Mistburned Barrens
        1595,  # Shipwreck Strand
        1593,  # Starlit Weald
        1622,  # Eternity's Garden
        1633,  # Leyspring Hollows
    ],

    'festival': [
        922,  # Labyrinthine Cliffs
        929,  # The Crown Pavilion
    ],

    'homestead': [
        1558,  # Hearth's Glow
        1596,  # Comosus Isle
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
        # 1564,  # Mount Balrior
        1609,  # Guardian's Glade
        # 1638,  # Nexus of Eternity
    ],

    'raid_convergence': [
        1564,  # Mount Balrior
        1638,  # Nexus of Eternity
    ],

    'festival_raid': [
        1352,  # Secret Lair of the Snowmen
    ],

    'strike': [
        1332,  # Shiverpeaks Pass
        # 1339,  # Boneskinner
        # 1341,  # Fraenir of Jormag
        1346,  # Voice of the Fallen and Claw of the Fallen
        1359,  # Whisper of Jormag
        1368,  # Forging Steel
        1374,  # Cold War
        1432,  # Aetherblade Hideout
        1450,  # Xunlai Jade Junkyard
        1451,  # Kaineng Overlook
        1437,  # Harvest Temple
        1485,  # Old Lion's Court
        1515,  # Cosmic Observatory
        1520,  # Temple of Febe
    ],

    'public_instance': [
        943,  # The Tower of Nightmares
        1412,  # Dragonstorm
        1482,  # The Battle for Lion's Arch
        1480,  # The Twisted Marionette
        1523,  # Convergence: Outer Nayos
        # 1562,  # Convergence: Mount Balrior
        # 1627,  # Convergence: Nexus of Eternity
    ],

    'story': [
        335,  # Claw Island
        1268,  # Fahranur, the First City
    ],

    'lounge': [
        # 1465,  # Thousand Seas Pavilion
    ],

    'misc': [
        336,  # Chantry of Secrets
        # 1397,  # Dragon Response Mission: Metrica Province
        # 1399,  # Dragon Response Mission: Brisban Wildlands
        # 1396,  # Dragon Response Mission: Gendarran Fields
        # 1398,  # Dragon Response Mission: Fields of Ruin
        # 1395,  # Dragon Response Mission: Thunderhead Peaks
        # 1393,  # Dragon Response Mission: Lake Doric
        # 1389,  # Dragon Response Mission: Snowden Drifts
        # 1403,  # Dragon Response Mission: Caledon Forest
        # 1387,  # Dragon Response Mission: Bloodtide Coast
        # 1390,  # Dragon Response Mission: Fireheart Rise
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
    1591: {'mastery_region': 'Visions of Eternity', 'access_req': 'voe'},
}

"""
Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. This can also add custom data for the zones:
- label_rect: The continent rect bounds to display the zone label in. Useful if multiple labels would overlap.
- label_anchor: Two letter description for where in the zone or label rect we want to align the label. First letter is the horizontal alignment (l = left, m = middle, r = right),
second letter is vertical alignment (t = top, m = middle, b = bottom). Default is middle ('mm').
- label_size: Size multiplier for the labels.
- mastery_region: Mastery experience region, if it's different from the typical chronological map ID progression based on source_thresholds.
- access_req: Holds abbreviation for access requirement (expansion or Living World season, see source_thresholds). Can also be set to a list of strings, if multiple requirements must be met simultaneously.
"""
all_zone_data_overrides: dict[int, dict] = {
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
        'continent_id': 1,
        # Fractals are technically in the Mists, but we might want to display them on the overworld map as well
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
        'access_req': 'pof',
        'continent_rect': [[66298, 50786], [68218, 52354]]
    },
    1332: {  # Shiverpeaks Pass
        'continent_rect': [[59392, 19014], [59900, 20064]],
        'label_rect': [[57683, 19014], [59731, 20064]],
        'label_anchor': 'rm'
    },
    1343: {  # Bjora Marches
        'label_rect': [[54943, 16972], [57122, 19148]]
    },
    1346: {  # Sanctum Arena (Voice of the Fallen and Claw of the Fallen / Fraenir of Jormag / Boneskinner)
        'name': "Voice of the Fallen and Claw of the Fallen,\nFraenir of Jormag,\nBoneskinner",
        'continent_rect': [[57058, 17816], [57430, 18187]],
        'label_rect': [[57106, 15892], [64162, 17816]],
        'label_anchor': 'lb'
    },
    1352: {  # Secret Lair of the Snowmen
        'name': "Secret Lair of the Snowmen",
        'mastery_region': 'Central Tyria',
        'continent_rect': [[52268, 24384], [53504, 25664]],
        'label_rect': [[51116, 24384], [53420, 25664]],
        'label_anchor': 'rm',
        'access_req': 'gw2'
    },
    1359: {  # Whisper of Jormag
        'label_rect': [[53928, 19164], [55464, 19724]],
        'label_anchor': 'rt'
    },
    1368: {  # Forging Steel
        'name': "Forging Steel"
    },
    1370: {  # Eye of the North
        'continent_rect': [[57344, 21248], [58198, 22102]]
    },
    1371: {  # Drizzlewood Coast
        'label_rect': [[50128, 17809], [52304, 20192]],
        'label_anchor': 'mb'
    },
    1374: {  # Cold War
        'continent_rect': [[51100, 20448], [51509, 20841]],
        'label_rect': [[50588, 20905], [52021, 21417]],
        'label_anchor': 'mt'
    },
    1419: {  # Isle of Reflection
        'continent_rect': [[21319, 103785], [23239, 105705]]
    },
    1422: {  # Dragon's End
        'label_rect': [[33126, 101838], [35302, 103758]],
        'label_anchor': 'mb'
    },
    1428: {  # Arborstone
        'continent_rect': [[29185, 100890], [30141, 101657]]
    },
    1432: {  # Aetherblade Hideout
        'label_rect': [[22576, 102796], [25008, 103340]],
        'label_anchor': 'mt'
    },
    1450: {  # Xunlai Jade Junkyard
        'continent_rect': [[30751, 101830], [31324, 102296]],
        'label_rect': [[30783, 101286], [33855, 101846]],
        'label_anchor': 'lb'
    },
    1451: {  # Kaineng Overlook
        'continent_rect': [[25829, 99853], [26153, 100177]],
        'label_rect': [[24807, 100209], [27175, 100721]],
        'label_anchor': 'mt'
    },
    1452: {  # The Echovald Wilds
        'label_rect': [[29185, 102296], [33025, 103450]]
    },
    1437: {  # Harvest Temple
        'continent_rect': [[33874, 104306], [34474, 104906]],
        'label_rect': [[31762, 104306], [33810, 104906]],
        'label_anchor': 'rm'
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
    1515: {  # Cosmic Observatory
        'continent_rect': [[26810, 23005], [27302, 23497]],
    },
    1520: {  # Temple of Febe
        'continent_rect': [[24108, 22416], [24108, 22416]],
    },
    1575: {  # Mistburned Barrens
        'continent_rect': [[34063, 10361], [35720, 12921]],
        'label_rect': [[34127, 10361], [35656, 12921]],
        'label_size': 0.9,
    },
    1595: {  # Shipwreck Strand
        'label_rect': [[9530, 58153], [12090, 60585]],
    },
    1609: {  # Guardian's Glade
        'continent_rect': [[9727, 58208], [10142, 58637]],
        'label_rect': [[8910, 57232], [10959, 58217]],
        'label_anchor': 'mb'
    },
}

"""Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. Similar to zone_data_overrides, but it includes additional changes for 
specific map overlays."""
conditional_zone_data_overrides: dict[type, dict[int, dict]] = {
    ZoneMapOverlay: {
        26: {  # Dredgehaunt Cliffs
            'label_rect': [[52672, 32524], [54080, 33664]],
        },
        27: {  # Lornar's Pass
            'label_rect': [[50720, 29696], [51968, 32134]],
            'label_anchor': 'mm',
        },
        36: {  # Ascalonian Catacombs
            'label_rect': [[61248, 29024], [62656, 30048]],
            'label_anchor': 'lb'
        },
        50: {  # Lion's Arch
            'label_size': 0.9
        },
        64: {  # Sorrow's Embrace
            'label_rect': [[52704, 33792], [55232, 34816]],
            'label_anchor': 'lt',
            'label_size': 0.7
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
            'label_rect': [[48512, 33600], [49920, 35456]],
        },
        76: {  # Caudecus's Manor
            'label_rect': [[43984, 28144], [45818, 28800]],
            'label_anchor': 'rm'
        },
        82: {  # Crucible of Eternity
            'label_rect': [[53952, 37728], [55328, 38592]],
            'label_anchor': 'lb'
        },
        139: {  # Rata Sum
            'continent_rect': [[37376, 36096], [39936, 38654]],
            'label_rect': [[37376, 37438], [39936, 38718]],
            'label_anchor': 'mt',
        },
        335: {  # Claw Island
            'label_size': 0.7
        },
        336: {  # Chantry of Secrets
            'label_rect': [[48640, 33312], [49920, 33856]],
            'label_size': 0.7,
            'label_anchor': 'mt',
        },
        872: {  # Fractals of the Mists
            'continent_rect': [[49392.2, 31889.7], [49392.2, 31889.7]],
            'label_rect': [[46208, 31788], [48990, 32252]],
            'label_anchor': 'rt',
            'label_size': 0.6
        },
        1043: {  # Auric Basin
            'label_rect': [[33408, 33856], [35200, 35328]],
            'label_anchor': 'mt',
        },
        1155: {  # Lion's Arch Aerodrome
            'continent_rect': [[49054, 31868], [49641, 32374]],
            'label_rect': [[49705, 31868], [51241, 32310]],
            'label_anchor': 'lm',
            'label_size': 0.6
        },
        1264: {  # Hall of Chains
            'continent_rect': [[51935.2, 32267.7], [51935.2, 32267.7]],
            'label_rect': [[52128, 32011.7], [54784, 32523.7]],
            'label_anchor': 'lb',
            'label_size': 0.7
        },
        1268: {  # Fahranur, the First City
            'label_rect': [[52048, 61488], [53904, 62768]],
            'label_size': 0.8
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[49331.4, 32136.9], [49331.4, 32136.9]],
            'label_rect': [[46208, 32252], [49014, 32748]],
            'label_anchor': 'rt',
            'label_size': 0.6
        },
        1368: {  # Forging Steel
            'continent_rect': [[57621.8, 21596.3], [57621.8, 21596.3]],
            'label_rect': [[57862, 21116], [59862, 21660]],
            'label_anchor': 'lb'
        },
        1370: {  # Eye of the North
            'label_rect': [[54944, 21248], [57248, 22102]],
            'label_anchor': 'rm',
            'access_req': 'gw2'
        },
        1412: {  # Dragonstorm
            'label_rect': [[51776, 26112], [53696, 27648]]
        },
        1428: {  # Arborstone
            'label_rect': [[26817, 100890], [29121, 101657]],
            'label_anchor': 'rm',
            'label_size': 0.9
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[50678, 32582], [51835, 33170]],
            'label_size': 0.7,
            'label_anchor': 'rt'
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The Battle for Lion's Arch",
            'continent_rect': [[48064, 30784], [50368, 32192]],
            'label_rect': [[46208, 30816], [48256, 31296]],
            'label_anchor': 'rt',
            'label_size': 0.6
        },
        1485: {  # Old Lion's Court
            'continent_rect': [[49006.9, 31189.1], [49006.9, 31189.1]],
            'label_rect': [[46208, 31296], [48256, 31776]],
            'label_anchor': 'rt',
            'label_size': 0.6
        },
        1509: {  # The Wizard's Tower
            'label_rect': [[24839, 21882], [28071, 22682]],
            'label_anchor': 'lm',
            'label_size': 0.9
        },
        1523: {  # Convergence: Outer Nayos
            'name': "Convergence: Outer Nayos",
            'continent_rect': [[24108, 22416], [24108, 22416]],
            'label_rect': [[21676, 21968], [23868, 22720]],
            'label_anchor': 'rt',
            'label_size': 0.8
        },
        1596: {  # Comosus Isle
            'label_rect': [[9844, 55500], [12020, 56908]],
            'access_req': ['jw', 'voe'],
        },
        1638: {  # Nexus of Eternity
            'continent_rect': [[4633, 58059], [4633, 58059]],
            'label_rect': [[3448, 56907], [5818, 57907]],
            'label_anchor': 'mb'
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
            'continent_rect': [[46336, 31568], [48192, 32208]],
            'label_rect': [[46208, 31632], [48320, 32208]],
            'label_size': 0.7
        },
        1185: {  # Lake Doric
            'label_size': 0.9
        },
        1264: {  # Hall of Chains
            'continent_rect': [[51840, 31996], [53760, 32636]],
            'label_size': 0.7
        },
        1268: {  # Fahranur, the First City
            'label_size': 0.8
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[48192, 32000], [50240, 32640]],
            'label_rect': [[47744, 32000], [50688, 32640]],
            'label_size': 0.7
        },
        1368: {  # Forging Steel
            'continent_rect': [[58262, 20939], [60006, 21643]],
            'label_rect': [[58358, 20939], [60006, 21643]],
            'label_anchor': 'lm'
        },
        1370: {  # Eye of the North
            'label_rect': [[56086, 21248], [58102, 22102]],
            'label_anchor': 'rm',
            'mastery_region': 'Central Tyria',
            'label_size': 0.9
        },
        1428: {  # Arborstone
            'label_rect': [[28929, 100890], [30397, 101657]],
            'label_size': 0.9
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[50646, 32249], [51776, 33170]],
            'label_anchor': 'rm',
            'label_size': 0.7
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The Battle for Lion's Arch",
            'continent_rect': [[47640, 30288], [50536, 30928]],
            'label_rect': [[47640, 30352], [50536, 30928]],
            'label_size': 0.7
        },
        1485: {  # Old Lion's Court
            'continent_rect': [[46336, 30928], [48192, 31568]],
            'label_rect': [[46208, 30992], [48320, 31568]],
            'label_size': 0.7
        },
        1509: {  # The Wizard's Tower
            'label_rect': [[23271, 21882], [24935, 22650]],
            'label_size': 0.9
        },
        1515: {  # Cosmic Observatory
            # 'continent_rect': [[27302, 22650], [29866, 23434]],
        },
        1520: {  # Temple of Febe
            # 'continent_rect': [[19691, 24076], [21871, 24860]],
        },
        1523: {  # Convergence: Outer Nayos
            'name': "Convergence:\nOuter Nayos",
            'continent_rect': [[19691, 20876], [21871, 21900]],
            'label_size': 0.75
        },
        1564: {  # Mount Balrior
            'label_size': 0.9
        },
        1638: {  # Nexus of Eternity
            'continent_rect': [[3538, 56665], [5922, 57385]]
        },
    }
}

"""Map IDs to ignore for specific map overlays."""
conditional_zone_blacklist: dict[type, list[int]] = {
    MasteryRegionMapOverlay: [
        336,  # Chantry of Secrets
        1155,  # Lion's Arch Aerodrome
    ]
}

conditional_custom_zones: dict[type, list[dict]] = {
    ZoneMapOverlay: [
        {
            'name': "Dragon Response Missions",
            'category': 'misc',
            'continent_rect': [[57853.3, 21830.8], [57853.3, 21830.8]],
            'label_rect': [[58093, 21718], [60029, 22342]],
            'label_anchor': 'lt',
            'mastery_region': 'Icebrood Saga',
            'access_req': 'lw5',
        },
    ],
    MasteryRegionMapOverlay: [
        {
            'name': "Dragon Response Missions",
            'category': 'misc',
            'continent_rect': [[58262, 21707], [61590, 22411]],
            'label_rect': [[58358, 21707], [61590, 22411]],
            'label_anchor': 'lm',
            'mastery_region': 'Icebrood Saga',
            'access_req': 'lw5',
        },
    ],
}
