from typing import Any

from gw2api import GuildWars2Client
from gw2api.objects.api_version_2 import Maps

from data.zones import zone_ids, zone_data_overrides

gw2_client: Any = GuildWars2Client()
max_page_size = 200


def load_zone_data(use_overrides: bool) -> list[dict]:
    maps_api: Maps = gw2_client.maps

    all_zone_ids = [zone_id for zone_id_list in zone_ids.values() for zone_id in zone_id_list]
    zone_categories_by_id = {zone_id: zone_category for (zone_category, zone_id_list) in zone_ids.items() for zone_id in zone_id_list}

    zones = []

    for ids in split_list(all_zone_ids, max_page_size):
        for m in maps_api.get(ids=ids):
            zone_id = m['id']
            zone_data = (m | zone_data_overrides[zone_id]) if use_overrides and zone_id in zone_data_overrides else m
            zone_data['category'] = zone_categories_by_id[zone_id]
            zones.append(zone_data)

    return zones


def split_list(input_list, sublist_size):
    return [input_list[i:i + sublist_size] for i in range(0, len(input_list), sublist_size)]
