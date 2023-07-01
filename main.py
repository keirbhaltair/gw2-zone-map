from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from gw2api import GuildWars2Client
from gw2api.objects.api_version_2 import Maps

from data import maps


def main():
    args = parse_arguments()
    map_data = load_map_data()
    generate_maps(args, map_data)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--tiles', default='tiles', help="The input tiles directory, such as from that_shaman's map API")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-z', '--zoom', nargs='+', type=int, default=[2], help="The zoom levels to generate the maps for")
    return parser.parse_args()


def load_map_data():
    def split_list(input_list, sublist_size):
        return [input_list[i:i + sublist_size] for i in range(0, len(input_list), sublist_size)]

    page_size = 200
    gw2_client: Any = GuildWars2Client()
    maps_api: Maps = gw2_client.maps
    map_ids = maps.MapList().get_all_ids()
    maps_for_display = []

    for ids in split_list(map_ids, page_size):
        for m in maps_api.get(ids=ids):
            if ('continent_id' in m and m['continent_id'] == 1
                    and 'type' in m and m['type'] == 'Public'
                    and 'floors' in m and 1 in m['floors']):
                maps_for_display.append(m)

    return maps_for_display


def generate_maps(args, map_data):
    tile_image_size = 256
    tile_coord_size_zoom_1 = 2 ** 14
    font = ImageFont.truetype("arial.ttf", 16)

    continent = 1
    floor = 1

    # Prepare output directory
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)
    for file in output_path.glob('*'):
        if file.is_file():
            file.unlink()

    # Load and combine the tiles into the image
    for zoom in args.zoom:
        tile_coord_size = tile_coord_size_zoom_1 / (2 ** (zoom - 1))
        tile_coord_multiplier = tile_image_size / tile_coord_size
        max_x, max_y = get_tile_count(args, continent, floor, zoom)
        image = Image.new("RGB", (tile_image_size * max_x, tile_image_size * max_y))
        draw = ImageDraw.Draw(image)

        # Merge tiles into the output image
        for x in range(max_x):
            for y in range(max_y):
                tile = Image.open(get_tile_path(args, continent, floor, zoom, x, y))
                image.paste(tile, (x * tile_image_size, y * tile_image_size))

        # Draw map boundaries
        for m in map_data:
            rect = m['continent_rect']
            image_rect = (rect[0][0] * tile_coord_multiplier, rect[0][1] * tile_coord_multiplier, rect[1][0] * tile_coord_multiplier, rect[1][1] * tile_coord_multiplier)
            draw.rectangle(image_rect, outline='white', width=1)
            image_rect_center = ((image_rect[0] + image_rect[2]) / 2, (image_rect[1] + image_rect[3]) / 2)
            draw.text(image_rect_center, m['name'], fill='white', font=font, anchor='mm')

        image.save(f'{args.output}/map_{zoom}.png')
        print(f"Finished zoom {zoom}.")


def get_tile_count(args, continent: int, floor: int, zoom: int):
    try:
        max_x = sum(1 for _ in Path(get_tile_path(args, continent, floor, zoom)).iterdir())
        max_y = max(sum(1 for _ in Path(get_tile_path(args, continent, floor, zoom, x)).iterdir()) for x in range(max_x))
        return max_x, max_y
    except FileNotFoundError as e:
        raise ValueError(f"Input tiles not found at: {get_tile_path(args)}.") from e


def get_tile_path(args, continent: int = None, floor: int = None, zoom: int = None, x: int = None, y: int = None):
    parts = [str(args.tiles)]
    for part in [continent, floor, zoom, x, y]:
        if part is None:
            break
        parts.append(str(part))
    return '/'.join(parts) if y is None else '/'.join(parts) + ".jpg"


if __name__ == '__main__':
    main()
