from argparse import ArgumentParser

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
    parser.add_argument('--lang', default='en', help="Language to generate the map in (en, es, de, fr). Default is en. (Not fully supported yet.)")
    parser.add_argument('--no-overrides', dest='overrides', action='store_false',
                        help="Marks if custom zone data overrides to the official API should be ignored (by default they are applied).")
    parser.add_argument('--no-legend', dest='legend', action='store_false', help="Marks if the overlay legends should be generated.")

    args = parser.parse_args()
    if not args.continent and not args.layout:
        setattr(args, 'layout', 'TyriaWorld')

    print(f"Arguments: {args}")
    return args


def generate_maps(args):
    tile_source = LocalMapTileSource(args.tiles)
    map_generator = MapGenerator(tile_source)
    map_overlay = ZoneMapOverlay()
    map_layout = choose_map_layout(args)

    print(f"Loading data from the API...")
    zone_data = load_zone_data(args.overrides, args.lang)
    print(f"Data loaded.")

    for zoom in args.zoom:
        print(f"Generating map for zoom {zoom}...")
        part_images = []

        map_coord = None
        for part in map_layout.parts:
            sector = part[1]
            map_params = continent_map_params[sector.continent_id]
            map_coord = MapCoordinateSystem(map_params, zoom, sector)

            part_image = map_generator.generate_map_image(sector.continent_id, 1, map_coord)
            map_overlay.draw_overlay(part_image, zone_data, map_coord)

            part_top_left = map_coord.continent_to_full_image_coord(part[0])
            part_images.append((part_top_left, part_image))

        output_file_name = f'continent{args.continent}' if args.continent else args.layout
        output_path = f'{args.output}/{output_file_name}_zones_zoom{zoom}_{args.lang}.png'
        full_image = part_images[0][1] if len(part_images) == 1 else combine_part_images(part_images)

        if args.legend:
            map_overlay.draw_legend(full_image, map_layout, map_coord)

        full_image.save(output_path)

        print(f"Map for zoom {zoom} finished.")


def choose_map_layout(args) -> MapLayout:
    if args.continent:
        return MapLayout.single_sector(MapSector(args.continent, None))
    elif args.layout:
        if args.layout not in map_layouts:
            raise ValueError(f"Invalid map layout name '{args.layout}' supplied, available values: {list(map_layouts.keys())}")
        return map_layouts[args.layout]
    else:
        raise ValueError('No continent or layout chosen.')


if __name__ == '__main__':
    main()
