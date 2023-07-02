from typing import Any

from gw2api import GuildWars2Client
from gw2api.objects.api_version_2 import Maps

city_ids = [
    18,  # Divinity's Reach
    50,  # Lion's Arch
    91,  # The Grove
    139,  # Rata Sum
    218,  # Black Citadel
    326,  # Hoelbrak
    1370,  # Eye of the North
    1428,  # Arborstone
]

open_world_ids = [
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
]

guild_hall_ids = [
    1068,  # Gilded Hollow
    1069,  # Lost Precipice
    1214,  # Windswept Haven
    1419,  # Isle of Reflection
]

dungeon_ids = [
    36,  # Ascalonian Catacombs
    76,  # Caudecus's Manor
    67,  # Twilight Arbor
    64,  # Sorrow's Embrace
    69,  # Citadel of Flame
    71,  # Honor of the Waves
    82,  # Crucible of Eternity
    112,  # The Ruined City of Arah
]

raid_ids = [
    1062,  # Spirit Vale
    1149,  # Salvation Pass
    1156,  # Stronghold of the Faithful
    1188,  # Bastion of the Penitent
    # 1264,  # Hall of Chains
    # 1303,  # Mythwright Gambit
    1323,  # The Key of Ahdashim
]

special_zone_ids = [
    335,  # Claw Island
    922,  # Labyrinthine Cliffs
    1268,  # Fahranur, the First City
]


def get_all_zone_ids():
    return open_world_ids + city_ids + guild_hall_ids + dungeon_ids + raid_ids + special_zone_ids


class ZoneData:
    def __init__(self, zone_response_data):
        self.id = zone_response_data['id']
        self.name = zone_response_data['name']
        self.min_level = zone_response_data['min_level']
        self.max_level = zone_response_data['max_level']
        self.type = zone_response_data['type']
        self.region_id = zone_response_data['region_id']
        self.region_name = zone_response_data['region_name']
        self.continent_id = zone_response_data['continent_id']
        self.continent_name = zone_response_data['continent_name']
        self.map_rect = zone_response_data['map_rect']
        self.continent_rect = zone_response_data['continent_rect']


class DataApi:
    _gw2_client: Any = GuildWars2Client()
    _maps_api: Maps = _gw2_client.maps

    _max_page_size = 200

    @staticmethod
    def load_zone_data() -> list[ZoneData]:
        zone_ids = get_all_zone_ids()
        zones = []

        for ids in DataApi._split_list(zone_ids, DataApi._max_page_size):
            for m in DataApi._maps_api.get(ids=ids):
                zones.append(ZoneData(m))

        return zones

    @staticmethod
    def _split_list(input_list, sublist_size):
        return [input_list[i:i + sublist_size] for i in range(0, len(input_list), sublist_size)]
