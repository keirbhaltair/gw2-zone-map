from mapgen.map_overlay import ZoneMapOverlay

zone_ids: dict[str, list[int]] = {
    'city': [
        18,  # Divinity's Reach
        50,  # Lion's Arch
        91,  # The Grove
        139,  # Rata Sum
        218,  # Black Citadel
        326,  # Hoelbrak
        1155,  # Lion's Arch Aerodrome
        1370,  # Eye of the North
        1428,  # Arborstone
        1465,  # Thousand Seas Pavilion
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
        922,  # Labyrinthine Cliffs
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

    'story': [
        335,  # Claw Island
        1268,  # Fahranur, the First City
    ],

    'misc': [
        336,  # Chantry of Secrets
    ],
}

"""
Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. This can also add custom data for the zones:
- label_rect: The continent rect bounds to display the zone label in. Useful if multiple labels would overlap.
- label_anchor: Two letter description for where in the zone or label rect we want to align the label. First letter is the horizontal alignment (l = left, m = middle, r = right),
second letter is vertical alignment (t = top, m = middle, b = bottom). Default is middle ('mm').
"""
zone_data_overrides: dict[int: dict] = {
    335: {  # Claw Island
        'continent_rect': [[46720, 32256], [48000, 33792]]
    },
    336: {  # Chantry of Secrets
        'continent_rect': [[48896, 32576], [49664, 33280]],
        'label_rect': [[49696, 32576], [50720, 33280]],
        'label_anchor': 'lm'
    },
    988: {  # Dry Top
        'continent_rect': [[36608, 32128], [38656, 33536]]
    },
    1062: {  # Spirit Vale
        'continent_rect': [[36392, 28544], [37112, 30592]],
        'label_rect': [[37000, 28592], [38504, 29696]],
        'label_anchor': 'lt'
    },
    1069: {  # Lost Precipice
        'label_rect': [[32224, 29696], [33504, 30976]],
        'label_anchor': 'rm'
    },
    1149: {  # Salvation Pass
        'continent_rect': [[35582, 28544], [36392, 30338]],
        'label_rect': [[35710, 28592], [36264, 30306]],
        'label_anchor': 'mt'
    },
    1155: {  # Lion's Arch Aerodrome
        'continent_rect': [[49054, 31868], [49641, 32374]],
        'label_rect': [[47006, 31804], [49022, 32438]],
        'label_anchor': 'rm'
    },
    1156: {  # Stronghold of the Faithful
        'continent_rect': [[34729, 28544], [35582, 30338]],
        'label_rect': [[33076, 28592], [34885, 29696]],
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
    1419: {  # Isle of Reflection
        'continent_rect': [[21319, 103785], [23239, 105705]]
    },
    1428: {  # Arborstone
        'continent_rect': [[29185, 100890], [30141, 101657]]
    },
    1465: {  # Thousand Seas Pavilion
        'continent_rect': [[20900, 98253], [22052, 99405]]
    },
}

"""Map IDs to ignore for specific map overlays."""
conditional_zone_blacklist: dict[type, list[int]] = {
    ZoneMapOverlay: [
        1264,  # Hall of Chains
        1303,  # Mythwright Gambit
    ]
}

"""Custom overrides for the data coming from the API to make the resulting map look a bit cleaner. Similar to zone_data_overrides, but it includes additional changes for 
specific map overlays."""
conditional_zone_data_overrides: dict[type, dict[int: dict]] = {
    ZoneMapOverlay: {
        27: {  # Lornar's Pass
            'label_rect': [[50432, 29696], [52224, 32938]]
        },
        36: {  # Ascalonian Catacombs
            'label_rect': [[61184, 29056], [62464, 30080]],
            'label_anchor': 'lm'
        },
        50: {  # Lion's Arch
            'label_rect': [[46976, 30720], [48736, 31804]],
            'label_anchor': 'rm'
        },
        64: {  # Sorrow's Embrace
            'label_rect': [[53696, 33792], [55232, 35328]],
            'label_anchor': 'lm'
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
        1043: {  # Auric Basin
            'label_rect': [[33280, 32896], [35328, 35328]]
        },
        1264: {  # Hall of Chains
            'label_rect': [[52352, 31484], [54784, 32508]],
            'label_anchor': 'lb'
        },
        1370: {  # Eye of the North
            'continent_rect': [[57344, 21248], [58198, 22102]],
            'label_rect': [[55008, 21248], [57312, 22102]],
            'label_anchor': 'rm'
        },
        1428: {  # Arborstone
            'label_rect': [[27585, 100890], [29121, 101657]],
            'label_anchor': 'rm'
        },
    }
}
