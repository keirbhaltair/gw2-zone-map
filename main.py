from argparse import ArgumentParser
from pathlib import Path

from data.continents import continent_map_params
from data.zones import DataApi
from map.map_generator import MapGenerator, LocalMapTileSource
from map.map_overlay import ZoneBoundaryOverlay


def main():
    args = parse_arguments()
    zone_data = DataApi.load_zone_data()
    generate_maps(args, zone_data)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--tiles', default='tiles', help="The input tiles directory, such as from that_shaman's map API")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-z', '--zoom', nargs='+', type=int, default=[1, 3], help="The zoom levels to generate the maps for")
    return parser.parse_args()


def generate_maps(args, zone_data):
    prepare_output_directory(args)

    continent_id = 1
    floor_id = 1

    map_params = continent_map_params[continent_id]
    tile_source = LocalMapTileSource(args.tiles)
    map_generator = MapGenerator(map_params, tile_source)
    map_overlay = ZoneBoundaryOverlay()

    for zoom in args.zoom:
        image = map_generator.generate_map_image(continent_id, floor_id, zoom)
        map_overlay.draw_overlay(image, map_params, zoom, zone_data)
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
