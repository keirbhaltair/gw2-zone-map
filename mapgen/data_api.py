import copy
import json
import os.path
from pathlib import Path
from typing import Literal

import requests

from data.zones import zone_ids, source_thresholds

max_page_size = 200
Language = Literal['en', 'es', 'de', 'fr']

maps_url = "https://api.guildwars2.com/v2/maps"
maps_cache_dir = 'api-cache'
maps_cache_path = os.path.join(maps_cache_dir, 'maps.json')


def load_zone_data(lang: Language = 'en', save_api_cache: bool = False, load_api_cache: bool = False) -> list[dict]:
    all_zone_ids = [zone_id for zone_id_list in zone_ids.values() for zone_id in zone_id_list]
    zone_categories_by_id = {zone_id: zone_category for (zone_category, zone_id_list) in zone_ids.items() for zone_id in zone_id_list}
    raw_zones = []
    zones = []

    if load_api_cache:
        print(f"Loading data from the local API cache at {maps_cache_path}...")
        map_data = load_cached_zone_data()
        map_data = [enhance_zone_data(m, zone_categories_by_id) for m in map_data]
        return map_data

    for ids in split_list(all_zone_ids, max_page_size):
        map_data = requests.get(maps_url, params={'ids': ','.join(str(i) for i in ids), 'lang': lang}).json()

        if save_api_cache:
            raw_zones.extend(copy.deepcopy(map_data))

        for m in map_data:
            enhanced_data = enhance_zone_data(m, zone_categories_by_id)
            zones.append(enhanced_data)

    if save_api_cache:
        print(f"Saving data to local API cache at {maps_cache_path}...")
        save_cached_zone_data(raw_zones)

    return zones


def enhance_zone_data(zone_data: dict, zone_categories_by_id: dict[int, str]) -> dict:
    zone_id = zone_data['id']
    zone_data['category'] = zone_categories_by_id[zone_id]
    return zone_data | source_thresholds[max(i for i in source_thresholds.keys() if i <= zone_id)]


def save_cached_zone_data(zones: list[dict]):
    if not zones:
        print("No zones to save.")
        return

    Path(maps_cache_dir).mkdir(parents=True, exist_ok=True)
    with open(maps_cache_path, 'w', encoding='utf-8') as f:
        json.dump(zones, f, ensure_ascii=False)


def load_cached_zone_data() -> list[dict]:
    if not os.path.exists(maps_cache_path):
        raise FileNotFoundError(f"API cache file {maps_cache_path} does not exist, please run the script with flag --api-save first.")

    with open(maps_cache_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
