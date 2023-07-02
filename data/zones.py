from typing import Any

from gw2api import GuildWars2Client
from gw2api.objects.api_version_2 import Maps

zone_ids = {
    'city': [
        18,  # Divinity's Reach
        50,  # Lion's Arch
        91,  # The Grove
        139,  # Rata Sum
        218,  # Black Citadel
        326,  # Hoelbrak
        # 1155,  # Lion's Arch Aerodrome
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
        # 1264,  # Hall of Chains
        # 1303,  # Mythwright Gambit
        1323,  # The Key of Ahdashim
    ],

    'story': [
        335,  # Claw Island
        1268,  # Fahranur, the First City
    ],
}

zone_data_overrides = {
    988: {  # Dry Top
        'continent_rect': [[36608, 32128], [38656, 33536]]
    },
    1062: {  # Spirit Vale
        'continent_rect': [[36392, 28544], [37112, 30592]]
    },
    1149: {  # Salvation Pass
        'continent_rect': [[35582, 28544], [36392, 30338]]
    },
    1155: {  # Lion's Arch Aerodrome
        'continent_rect': [[49054, 31868], [49641, 32374]]
    },
    1156: {  # Stronghold of the Faithful
        'continent_rect': [[34729, 28544], [35582, 30338]]
    },
    1175: {  # Ember Bay
        'continent_rect': [[37374, 44676], [41214, 47358]]
    },
    1195: {  # Draconis Mons
        'continent_rect': [[34716, 40034], [38560, 43134]]
    },
    1263: {  # Domain of Istan
        'continent_rect': [[55318, 59966], [58858, 63406]]
    },
    1288: {  # Domain of Kourna
        'continent_rect': [[63624, 59572], [67212, 63806]]
    },
    1428: {  # Arborstone
        'continent_rect': [[29185, 100890], [30141, 101657]]
    },
}


class DataApi:
    @staticmethod
    def load_zone_data(use_overrides: bool) -> list[dict]:
        gw2_client: Any = GuildWars2Client()
        maps_api: Maps = gw2_client.maps
        max_page_size = 200

        all_zone_ids = [zone_id for zone_id_list in zone_ids.values() for zone_id in zone_id_list]
        zone_categories_by_id = {zone_id: zone_category for (zone_category, zone_id_list) in zone_ids.items() for zone_id in zone_id_list}

        zones = []

        for ids in DataApi._split_list(all_zone_ids, max_page_size):
            for m in maps_api.get(ids=ids):
                zone_id = m['id']
                zone_data = (m | zone_data_overrides[zone_id]) if use_overrides and zone_id in zone_data_overrides else m
                zone_data['category'] = zone_categories_by_id[zone_id]
                zones.append(zone_data)

        print('Loaded zone data from the API.')

        return zones

    @staticmethod
    def _split_list(input_list, sublist_size):
        return [input_list[i:i + sublist_size] for i in range(0, len(input_list), sublist_size)]
