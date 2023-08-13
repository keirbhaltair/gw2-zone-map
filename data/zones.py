from mapgen.map_overlay import ZoneMapOverlay, MasteryRegionMapOverlay

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
        1370,  # Eye of the North
        1428,  # Arborstone
        # 1483,  # Memory of Old Lion's Arch
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
    ],

    'festival': [
        922,  # Labyrinthine Cliffs
        929,  # The Crown Pavilion
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
    ],

    'story': [
        335,  # Claw Island
        1268,  # Fahranur, the First City
    ],

    'hybrid_instance': [
        943,  # The Tower of Nightmares
        1412,  # Dragonstorm
        1482,  # The Battle for Lion's Arch
        1480,  # The Twisted Marionette
    ],

    'lounge': [
        1465,  # Thousand Seas Pavilion
    ],

    'misc': [
        336,  # Chantry of Secrets
    ],
}

source_thresholds = {
    0: {'mastery_region': 'Central Tyria'},
    1032: {'mastery_region': 'Heart of Thorns'},
    1209: {'mastery_region': 'Path of Fire'},
    1329: {'mastery_region': 'Icebrood Saga'},
    1415: {'mastery_region': 'End of Dragons'},
    1466: {'mastery_region': 'Central Tyria'},  # Living World Season 1 rework
    1488: {'mastery_region': 'End of Dragons'},
}

"""
Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. This can also add custom data for the zones:
- label_rect: The continent rect bounds to display the zone label in. Useful if multiple labels would overlap.
- label_anchor: Two letter description for where in the zone or label rect we want to align the label. First letter is the horizontal alignment (l = left, m = middle, r = right),
second letter is vertical alignment (t = top, m = middle, b = bottom). Default is middle ('mm').
- label_size: Size multiplier for the labels.
- mastery_region: Mastery experience region, if it's different from the typical chronological map ID progression based on source_thresholds.
"""
zone_data_overrides: dict[int: dict] = {
    23: {  # Kessex Hills
        'label_rect': [[44352, 30464], [45760, 32512]]
    },
    27: {  # Lornar's Pass
        'label_rect': [[50816, 30784], [51840, 31644]]
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
        'label_rect': [[41914, 26880], [42938, 27648]],
        'label_anchor': 'rm'
    },
    943: {  # The Tower of Nightmares
        'name': "The Tower of Nightmares",
        'continent_rect': [[42884, 31084], [43908, 32108]]
    },
    1043: {  # Auric Basin
        'label_rect': [[33280, 32896], [35328, 35328]]
    },
    1062: {  # Spirit Vale
        'continent_rect': [[36392, 28544], [37112, 30592]],
        'label_rect': [[36872, 28592], [38504, 29696]],
        'label_anchor': 'lt'
    },
    1069: {  # Lost Precipice
        'label_rect': [[32416, 29696], [34208, 30976]],
        'label_anchor': 'rm'
    },
    1149: {  # Salvation Pass
        'continent_rect': [[35582, 28544], [36392, 30338]],
        'label_rect': [[35710, 28592], [36264, 30306]],
        'label_anchor': 'mt'
    },
    1156: {  # Stronghold of the Faithful
        'continent_rect': [[34729, 28544], [35582, 30338]],
        'label_rect': [[33076, 28592], [35013, 29696]],
        'label_anchor': 'rt'
    },
    1175: {  # Ember Bay
        'continent_rect': [[37374, 44676], [41214, 47358]]
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
    1288: {  # Domain of Kourna
        'continent_rect': [[63624, 59576], [67212, 63806]]
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
        'label_size': 0.75
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
            'label_rect': [[52736, 32892], [54016, 33792]],
        },
        29: {  # Timberline Falls
            'label_rect': [[51712, 35328], [54016, 37760]]
        },
        36: {  # Ascalonian Catacombs
            'label_rect': [[61184, 29056], [62464, 30080]],
            'label_anchor': 'lm'
        },
        50: {  # Lion's Arch
            'label_rect': [[46976, 30752], [48736, 31804]],
            'label_anchor': 'rt'
        },
        64: {  # Sorrow's Embrace
            'label_rect': [[52352, 34688], [53376, 35328]],
            'label_anchor': 'mt'
        },
        67: {  # Twilight Arbor
            'label_rect': [[42560, 32704], [43456, 33728]],
            'label_anchor': 'lt'
        },
        69: {  # Citadel of Flame
            'label_rect': [[59968, 24064], [61248, 25344]],
            'label_anchor': 'lm'
        },
        71: {  # Honor of the Waves
            'label_rect': [[55424, 24448], [56576, 25600]],
            'label_anchor': 'lm'
        },
        76: {  # Caudecus's Manor
            'label_rect': [[44672, 27776], [45866, 28800]],
            'label_anchor': 'rm'
        },
        82: {  # Crucible of Eternity
            'label_rect': [[53952, 37312], [54976, 38592]],
            'label_anchor': 'lm'
        },
        139: {  # Rata Sum
            'continent_rect': [[37376, 36096], [39936, 38654]],
            'label_rect': [[37376, 36735], [39936, 38654]],
        },
        336: {  # Chantry of Secrets
            'label_rect': [[49696, 32288], [50720, 33120]],
            'label_anchor': 'lb',
            'label_size': 0.75
        },
        872: {  # Fractals of the Mists
            'continent_rect': [[49392.2, 31889.7], [49392.2, 31889.7]],
            'label_rect': [[47006, 31804], [49022, 32188]],
            'label_anchor': 'rb',
            'label_size': 0.75
        },
        1155: {  # Lion's Arch Aerodrome
            'continent_rect': [[49054, 31868], [49641, 32374]],
            'label_rect': [[47006, 32188], [49022, 32822]],
            'label_anchor': 'rt',
            'label_size': 0.75
        },
        1264: {  # Hall of Chains
            'continent_rect': [[51935.2, 32267.7], [51935.2, 32267.7]],
            'label_rect': [[52160, 32092], [54784, 32598]],
            'label_anchor': 'lm',
            'label_size': 0.75
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[49331.4, 32136.9], [49331.4, 32136.9]],
            'label_rect': [[49753, 31836], [51753, 32342]],
            'label_anchor': 'lm',
            'label_size': 0.75
        },
        1370: {  # Eye of the North
            'label_rect': [[55008, 21248], [57312, 22102]],
            'label_anchor': 'rm'
        },
        1428: {  # Arborstone
            'label_rect': [[27585, 100890], [29121, 101657]],
            'label_anchor': 'rm'
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[51382, 32946], [52128, 33522]],
            'label_anchor': 'rt',
            'label_size': 0.75
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The Battle for Lion's Arch",
            'continent_rect': [[48064, 30784], [50368, 32192]],
            'label_rect': [[49065, 30464], [50985, 30976]],
            'label_anchor': 'lb',
            'label_size': 0.75
        },
    },
    MasteryRegionMapOverlay: {
        17: {  # Harathi Hinterlands
            'label_rect': [[46208, 25856], [49408, 27990]],
        },
        26: {  # Dredgehaunt Cliffs
            'label_rect': [[52224, 32892], [54528, 33792]],
        },
        39: {  # Mount Maelstrom
            'label_rect': [[50560, 38720], [54400, 40192]],
        },
        50: {  # Lion's Arch
            'label_rect': [[48256, 30912], [50432, 32128]]
        },
        335: {  # Claw Island
            'continent_rect': [[46720, 32512], [48000, 33792]]
        },
        872: {  # Fractals of the Mists
            'continent_rect': [[46336, 30912], [48128, 31680]],
            'label_size': 0.75
        },
        1303: {  # Mythwright Gambit
            'continent_rect': [[46336, 31680], [48128, 32448]],
            'label_size': 0.75
        },
        1370: {  # Eye of the North
            'label_rect': [[57088, 21248], [58454, 22102]]
        },
        1432: {  # Aetherblade Hideout
            'continent_rect': [[23367, 103145], [25543, 104169]],
        },
        1437: {  # Harvest Temple
            'continent_rect': [[33382, 105550], [35046, 106574]],
        },
        1450: {  # Xunlai Jade Junkyard
            'continent_rect': [[30209, 99866], [32001, 100890]],
        },
        1451: {  # Kaineng Overlook
            'continent_rect': [[26024, 100660], [27816, 101684]],
        },
        1480: {  # The Twisted Marionette
            'label_rect': [[51030, 32249], [51776, 33170]],
            'label_anchor': 'rm',
            'label_size': 0.75
        },
        1482: {  # The Battle for Lion's Arch
            'name': "The Battle for Lion's Arch",
            'continent_rect': [[47616, 30144], [50560, 30912]],
            'label_size': 0.75
        },
        1485: {  # Old Lion's Court
            'continent_rect': [[48288, 32128], [50144, 33088]],
            'label_rect': [[48544, 32128], [49888, 33088]],
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
    ],
    MasteryRegionMapOverlay: [
        336,  # Chantry of Secrets
        1155,  # Lion's Arch Aerodrome
        1465,  # Thousand Seas Pavilion
    ],
}

conditional_custom_zones: dict[type, list[dict]] = {
    MasteryRegionMapOverlay: [
        {
            'name': '\n'.join([
                "Strike Missions:",
                "   Shiverpeaks Pass",
                "   Fraenir of Jormag",
                "   Voice of the Fallen and Claw of the Fallen",
                "   Boneskinner",
                "   Whisper of Jormag",
                "   Forging Steel",
                "   Cold War",
            ]),
            'category': 'strike',
            'continent_rect': [[59222, 20512], [62550, 23104]],
            'label_rect': [[59350, 20512], [65110, 23104]],
            'label_anchor': 'lm',
            'mastery_region': 'Icebrood Saga',
        },
        {
            'name': "Dragon Response Missions",
            'category': 'misc',
            'continent_rect': [[55382, 20288], [58838, 21056]],
            'mastery_region': 'Icebrood Saga',
        },
    ]
}
