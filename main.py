from argparse import ArgumentParser
from pathlib import Path

import data
import mapgen


def main():
    args = parse_arguments()
    generate_maps(args)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--tiles', default='tiles', help="The input tiles directory, such as from that_shaman's map API")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-z', '--zoom', nargs='+', type=int, default=[3], help="The zoom levels to generate the maps for")
    parser.add_argument('--no-overrides', dest='overrides', action='store_false',
                        help="Marks if custom zone data overrides to the official API should be ignored (by default they are applied).")
    return parser.parse_args()


def generate_maps(args):
    continent_id = 1
    floor_id = 1

    prepare_output_directory(args)

    tile_source = mapgen.map_generator.LocalMapTileSource(args.tiles)
    map_generator = mapgen.map_generator.MapGenerator(tile_source)
    map_overlay = mapgen.map_overlay.ZoneBoundaryOverlay()
    zone_data = mapgen.data_api.load_zone_data(args.overrides)

    map_params = data.continents.continent_map_params[continent_id]
    sector = data.sectors.sectors['Tyria']

    for zoom in args.zoom:
        map_coord = mapgen.map_coordinates.MapCoordinateSystem(map_params, zoom, sector)
        image = map_generator.generate_map_image(continent_id, floor_id, map_coord)
        map_overlay.draw_overlay(image, zone_data, map_coord)
        image.save(f'{args.output}/zoom_{zoom}.png')
        print(f"Finished zoom {zoom}.")


def prepare_output_directory(args):
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)
    for file in output_path.glob('*'):
        if file.is_file():
            file.unlink()


if __name__ == '__main__':
    main()
