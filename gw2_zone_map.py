from argparse import ArgumentParser
from pathlib import Path

from data.continents import continent_map_params
from data.layouts import map_layouts
from data.zones import conditional_zone_blacklist, conditional_zone_data_overrides, all_zone_data_overrides, \
    conditional_custom_zones
from mapgen.data_api import load_zone_data
from mapgen.map_composite import combine_part_images
from mapgen.map_coordinates import MapSector, MapCoordinateSystem, MapLayout
from mapgen.map_generator import MapGenerator
from mapgen.overlay import map_overlays
from mapgen.overlay.overlay_util import MapOverlay


def main():
    args = parse_arguments()
    generate_maps(args)


def parse_arguments():
    parser = ArgumentParser()

    sector_group = parser.add_mutually_exclusive_group()
    sector_group.add_argument('-c', '--continent', type=int, help="ID of the continent to generate the map for")
    sector_group.add_argument('-l', '--layout', nargs='+', help=f"Name of the layout to generate the map for. Allowed values are: {list(map_layouts.keys())}")

    parser.add_argument('-f', '--format', default='jpg', help="Output file format")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-s', '--scale', type=float, default=1, help="Overlay scaling factor, default is 1.")
    parser.add_argument('-t', '--tiles', default='api',
                        help="Source of map tile images. Allowed values are: 'local' (provided in a local directory structure, such as from that_shaman's map API), and 'api' (provided by the official tile API). Default is 'api'.")
    parser.add_argument('-v', '--overlay', nargs='+', default=['zone_access', 'mastery'], help=f"Map overlays to generate. Allowed values are: {list(map_overlays.keys())}")
    parser.add_argument('-z', '--zoom', nargs='+', type=float, default=[3.4],
                        help="The zoom levels to generate the maps for. Does support decimal numbers as long as the zoom level exists when rounded up.")
    parser.add_argument('--api-load', action='store_true', default=False,
                        help='Instead of the REST API, optionally loads the API data from a local cache located in the api-cache directory, previously saved by the --api-save parameter. Can be used when the API service is down.')
    parser.add_argument('--api-save', action='store_true', default=False,
                        help='Optionally saves the data downloaded from the REST API to the api-cache directory, to be loaded later by the --api-load parameter in case the API service is down.')
    parser.add_argument('--debug', action='store_true', help="Renders debugging overlays, such as text label regions.")
    parser.add_argument('--lang', default='en', help="Language to generate the map for (en, es, de, fr). Default is en. (Not fully supported yet.)")
    parser.add_argument('--no-legend', dest='legend', action='store_false', help="Marks if the overlay legends should be generated.")
    parser.add_argument('--no-overrides', dest='overrides', action='store_false',
                        help="Marks if custom zone data overrides to the official API should be ignored (by default they are applied).")
    parser.add_argument('--tiles-dir', default='tiles', help="If tiles are set to 'local', name of the input tiles directory, such as from that_shaman's map API.")

    args = parser.parse_args()
    if not args.continent and not args.layout:
        setattr(args, 'layout', ['TyriaWorld'])

    if args.api_save and args.api_load:
        raise RuntimeError("Cannot simultaneously save and load the API cache.")

    print(f"Arguments: {args}")
    return args


def generate_maps(args):
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    map_generator = MapGenerator(args)

    print(f"Loading data from the API...")
    zone_data = load_zone_data(args.lang, args.api_save, args.api_load)
    print(f"Data loaded.")

    for layout_name, map_layout in choose_map_layouts(args):
        for zoom in args.zoom:
            print(f"Generating maps for layout '{layout_name}' at zoom {zoom}...")
            part_images = {}

            map_coord = None
            scale_factor = args.scale
            for sector_index, part in enumerate(map_layout.parts, start=1):
                sector = part[1]
                map_params = continent_map_params[sector.continent_id]
                map_coord = MapCoordinateSystem(map_params, zoom, sector)
                part_top_left = map_coord.continent_to_full_image_coord(part[0], False)

                part_image = map_generator.generate_map_image(sector.continent_id, 1, map_coord, sector_index, len(map_layout.parts))

                for i, overlay_name in enumerate(args.overlay, start=1):
                    print(f"Drawing map overlay '{overlay_name}'...")
                    if overlay_name not in map_overlays:
                        raise ValueError(f"Invalid overlay name specified ({overlay_name}). Allowed values are: {list(map_overlays.keys())}")
                    map_overlay = map_overlays[overlay_name]
                    overridden_zone_data = override_zone_data(zone_data, map_overlay) if args.overrides else zone_data
                    part_image_copy = part_image.copy() if i < len(args.overlay) else part_image
                    map_overlay.draw_overlay(part_image_copy, overridden_zone_data, map_layout, map_coord, scale_factor,
                                             debug=args.debug)

                    if overlay_name not in part_images:
                        part_images[overlay_name] = []
                    part_images[overlay_name].append((part_top_left, part_image_copy))

                    print(f"Map overlay '{overlay_name}' finished.")

            for overlay_name in part_images.keys():
                zoom_text = str(zoom).replace('.', '-')
                output_path = f'{args.output}/{layout_name}_{overlay_name}_z{zoom_text}_{args.lang}.{args.format}'

                if len(part_images[overlay_name]) == 1:
                    full_image = part_images[overlay_name][0][1]
                else:
                    full_image = combine_part_images(part_images[overlay_name], map_coord, scale_factor)

                if args.legend:
                    map_overlays[overlay_name].draw_legend(full_image, map_layout, map_coord, scale_factor)

                full_image.save(output_path, quality=95 if args.format == 'jpg' else None)

            print(f"\nMaps for layout '{layout_name}' at zoom {zoom} finished.")


def choose_map_layouts(args) -> list[tuple[str, MapLayout]]:
    if args.continent:
        return [(f'continent{args.continent}', MapLayout.single_sector(MapSector(args.continent, None)))]
    elif args.layout:
        layouts = []
        for layout in args.layout:
            if layout not in map_layouts:
                raise ValueError(f"Invalid map layout name '{layout}' supplied, available values: {list(map_layouts.keys())}")
            layouts.append((layout, map_layouts[layout]))
        return layouts
    else:
        raise ValueError('No continent or layout chosen.')


def override_zone_data(zone_data: list[dict], map_overlay: MapOverlay):
    custom_data = []

    for z in zone_data:
        if type(map_overlay) in conditional_zone_blacklist and z['id'] in conditional_zone_blacklist[type(map_overlay)]:
            continue

        d = z | all_zone_data_overrides[z['id']] if z['id'] in all_zone_data_overrides else z

        if type(map_overlay) in conditional_zone_data_overrides and z['id'] in conditional_zone_data_overrides[type(map_overlay)]:
            d = d | conditional_zone_data_overrides[type(map_overlay)][z['id']]
        custom_data.append(d)

    if type(map_overlay) in conditional_custom_zones:
        for z in conditional_custom_zones[type(map_overlay)]:
            if 'id' not in z:
                z['id'] = -1
            custom_data.append(z)

    return custom_data


if __name__ == '__main__':
    main()
