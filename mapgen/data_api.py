from typing import Literal

import requests

from data.zones import zone_ids, source_thresholds

max_page_size = 200
Language = Literal['en', 'es', 'de', 'fr']

maps_url = "https://api.guildwars2.com/v2/maps"


def load_zone_data(lang: Language = 'en') -> list[dict]:
    all_zone_ids = [zone_id for zone_id_list in zone_ids.values() for zone_id in zone_id_list]
    zone_categories_by_id = {zone_id: zone_category for (zone_category, zone_id_list) in zone_ids.items() for zone_id in zone_id_list}
    zones = []

    for ids in split_list(all_zone_ids, max_page_size):
        map_data = requests.get(maps_url, params={'ids': ','.join(str(i) for i in ids), 'lang': lang}).json()
        for m in map_data:
            zone_id = m['id']
            m['category'] = zone_categories_by_id[zone_id]
            m = m | source_thresholds[max(i for i in source_thresholds.keys() if i <= zone_id)]
            zones.append(m)

    return zones


def split_list(input_list, sublist_size):
    return [input_list[i:i + sublist_size] for i in range(0, len(input_list), sublist_size)]


def print_all_zone_data():
    all_zone_ids = requests.get(maps_url).json()
    for ids in split_list(all_zone_ids, max_page_size):
        map_data = requests.get(maps_url, params={'ids': ','.join(str(i) for i in ids)}).json()
        for zone in map_data:
            print(f"id: {zone['id']}; name: {zone['name']}")


if __name__ == '__main__':
    print_all_zone_data()
