from argparse import ArgumentParser
from pathlib import Path

from data.continents import continent_map_params
from data.layouts import map_layouts
from mapgen.data_api import load_zone_data
from mapgen.map_composite import combine_part_images
from mapgen.map_coordinates import MapCoordinateSystem, MapLayout, MapSector
from mapgen.map_generator import LocalMapTileSource, MapGenerator
from mapgen.map_overlay import ZoneMapOverlay


def main():
    args = parse_arguments()
    generate_maps(args)


def parse_arguments():
    parser = ArgumentParser()

    sector_group = parser.add_mutually_exclusive_group()
    sector_group.add_argument('-c', '--continent', type=int, help="ID of the continent to generate the map for")
    sector_group.add_argument('-l', '--layout', help="Name of the layout to generate the map for")

    parser.add_argument('-t', '--tiles', default='tiles', help="The input tiles directory, such as from that_shaman's map API")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-z', '--zoom', nargs='+', type=int, default=[3], help="The zoom levels to generate the maps for")
    parser.add_argument('--no-overrides', dest='overrides', action='store_false',
                        help="Marks if custom zone data overrides to the official API should be ignored (by default they are applied).")

    return parser.parse_args()


def generate_maps(args):
    prepare_output_directory(args)

    tile_source = LocalMapTileSource(args.tiles)
    map_generator = MapGenerator(tile_source)
    map_overlay = ZoneMapOverlay()
    map_layout = choose_map_layout(args)
    zone_data = load_zone_data(args.overrides)

    for zoom in args.zoom:
        part_images = []

        for part in map_layout.parts:
            sector = part[1]
            map_params = continent_map_params[sector.continent_id]
            map_coord = MapCoordinateSystem(map_params, zoom, sector)

            part_image = map_generator.generate_map_image(sector.continent_id, 1, map_coord)
            map_overlay.draw_overlay(part_image, zone_data, map_coord)

            part_top_left = map_coord.continent_to_full_image_coord(part[0])
            part_images.append((part_top_left, part_image))

        output_file_name = f'{args.output}/zoom_{zoom}.png'
        if len(part_images) == 1:
            part_images[0][1].save(output_file_name)
        else:
            combine_part_images(part_images).save(output_file_name)

        print(f"Finished zoom {zoom}.")


def prepare_output_directory(args):
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)
    for file in output_path.glob('*'):
        if file.is_file():
            file.unlink()


def choose_map_layout(args) -> MapLayout:
    if args.continent:
        return MapLayout.single_sector(MapSector(args.continent, None))
    elif args.layout:
        if args.layout not in map_layouts:
            raise ValueError(f"Invalid map layout name '{args.layout}' supplied, available values: {list(map_layouts.keys())}")
        return map_layouts[args.layout]
    else:
        return map_layouts['TyriaWorld']  # Default setting if nothing else was chosen


if __name__ == '__main__':
    main()
