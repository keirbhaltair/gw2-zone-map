from argparse import ArgumentParser
from pathlib import Path

from data.continents import continent_map_params
from data.layouts import map_layouts
from data.zones import conditional_zone_blacklist, conditional_zone_data_overrides, all_zone_data_overrides, conditional_custom_zones
from mapgen.data_api import load_zone_data
from mapgen.map_composite import combine_part_images
from mapgen.map_coordinates import MapSector, MapCoordinateSystem, MapLayout
from mapgen.map_generator import LocalMapTileSource, MapGenerator
from mapgen.overlay import map_overlays
from mapgen.overlay.overlay_util import MapOverlay


def main():
    args = parse_arguments()
    generate_maps(args)


def parse_arguments():
    parser = ArgumentParser()

    sector_group = parser.add_mutually_exclusive_group()
    sector_group.add_argument('-c', '--continent', type=int, help="ID of the continent to generate the map for")
    sector_group.add_argument('-l', '--layout', help=f"Name of the layout to generate the map for. Allowed values are: {list(map_layouts.keys())}")

    parser.add_argument('-t', '--tiles', default='tiles', help="The input tiles directory, such as from that_shaman's map API")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-f', '--format', default='jpg', help="Output file format")
    parser.add_argument('-v', '--overlay', nargs='+', default=['zone_access', 'mastery'], help=f"Map overlays to generate. Allowed values are: {list(map_overlays.keys())}")
    parser.add_argument('-s', '--scale', type=float, default=1, help="Overlay scaling factor, default is 1.")
    parser.add_argument('-z', '--zoom', nargs='+', type=float, default=[3.6],
                        help="The zoom levels to generate the maps for. Does support decimal numbers as long as the zoom level exists when rounded up.")
    parser.add_argument('--lang', default='en', help="Language to generate the map for (en, es, de, fr). Default is en. (Not fully supported yet.)")
    parser.add_argument('--no-overrides', dest='overrides', action='store_false',
                        help="Marks if custom zone data overrides to the official API should be ignored (by default they are applied).")
    parser.add_argument('--no-legend', dest='legend', action='store_false', help="Marks if the overlay legends should be generated.")
    parser.add_argument('--debug', action='store_true', help="Renders debugging overlays, such as text label regions.")

    args = parser.parse_args()
    if not args.continent and not args.layout:
        setattr(args, 'layout', 'TyriaWorld')

    print(f"Arguments: {args}")
    return args


def generate_maps(args):
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)

    tile_source = LocalMapTileSource(args.tiles)
    map_generator = MapGenerator(tile_source)
    map_layout = choose_map_layout(args)

    print(f"Loading data from the API...")
    zone_data = load_zone_data(args.lang)
    print(f"Data loaded.")

    for zoom in args.zoom:
        print(f"Generating maps for zoom {zoom}...")
        part_images = {}

        map_coord = None
        scale_factor = args.scale
        for part in map_layout.parts:
            sector = part[1]
            map_params = continent_map_params[sector.continent_id]
            map_coord = MapCoordinateSystem(map_params, zoom, sector)
            part_top_left = map_coord.continent_to_full_image_coord(part[0], False)

            part_image = map_generator.generate_map_image(sector.continent_id, 1, map_coord)

            for i, overlay_name in enumerate(args.overlay, start=1):
                if overlay_name not in map_overlays:
                    raise ValueError(f"Invalid overlay name specified ({overlay_name}). Allowed values are: {list(map_overlays.keys())}")
                map_overlay = map_overlays[overlay_name]
                overridden_zone_data = override_zone_data(zone_data, map_overlay) if args.overrides else zone_data
                part_image_copy = part_image.copy() if i < len(args.overlay) else part_image
                map_overlay.draw_overlay(part_image_copy, overridden_zone_data, map_coord, scale_factor, debug=args.debug)

                if overlay_name not in part_images:
                    part_images[overlay_name] = []
                part_images[overlay_name].append((part_top_left, part_image_copy))

        for overlay_name in part_images.keys():
            layout_name = f'continent{args.continent}' if args.continent else args.layout
            zoom_text = str(zoom).replace('.', '-')
            output_path = f'{args.output}/{layout_name}_{overlay_name}_z{zoom_text}_{args.lang}.{args.format}'

            if len(part_images[overlay_name]) == 1:
                full_image = part_images[overlay_name][0][1]
            else:
                full_image = combine_part_images(part_images[overlay_name], map_coord, scale_factor)

            if args.legend:
                map_overlays[overlay_name].draw_legend(full_image, map_layout, map_coord, scale_factor)

            full_image.save(output_path, quality=95 if args.format == 'jpg' else None)

        print(f"Maps for zoom {zoom} finished.")


def choose_map_layout(args) -> MapLayout:
    if args.continent:
        return MapLayout.single_sector(MapSector(args.continent, None))
    elif args.layout:
        if args.layout not in map_layouts:
            raise ValueError(f"Invalid map layout name '{args.layout}' supplied, available values: {list(map_layouts.keys())}")
        return map_layouts[args.layout]
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
