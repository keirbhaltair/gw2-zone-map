from PIL import Image
from pathlib import Path
import argparse


def main():
    args = parse_arguments()
    generate_maps(args)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tiles', default='input/tiles', help="The input tiles directory")
    parser.add_argument('-o', '--output', default='output', help="The output directory")
    parser.add_argument('-z', '--zoom', nargs='+', type=int, default=[2], help="The zoom levels to generate the maps for")
    return parser.parse_args()


def generate_maps(args):
    tile_size = 256
    continent = 1
    floor = 1

    # Prepare output directory
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)
    for file in output_path.glob('*'):
        if file.is_file():
            file.unlink()

    # Load and combine the tiles into the image
    for z in args.zoom:
        max_x, max_y = get_tile_count(args, continent, floor, z)
        image = Image.new("RGB", (tile_size * max_x, tile_size * max_y))
        for x in range(max_x):
            for y in range(max_y):
                tile = Image.open(get_tile_path(args, continent, floor, z, x, y))
                image.paste(tile, (x * tile_size, y * tile_size))

        image.save(f'{args.output}/map_{z}.png')
        print(f"Finished zoom {z}")


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
