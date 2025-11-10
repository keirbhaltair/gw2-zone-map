import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

import requests
from PIL import Image
from PIL.Image import Resampling
from requests import HTTPError

from mapgen.map_coordinates import tile_image_size, MapCoordinateSystem


class MapTileSource(ABC):
    @abstractmethod
    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image.Image:
        pass

    @abstractmethod
    def get_max_parallel_workers(self) -> int:
        pass


class LocalMapTileSource(MapTileSource):
    """Map tile source looking for tile images on the local file system, in the format of "continent/floor/zoom/x/y.jpg", for instance from that_shaman's mapgen API."""

    def __init__(self, input_directory: str):
        self.input_directory = input_directory

    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image.Image:
        return Image.open(f"{self.input_directory}/{continent}/{floor}/{zoom}/{x}/{y}.jpg")

    def get_max_parallel_workers(self) -> int:
        return 1


class TileApiMapTileSource(MapTileSource):
    """Map tile source looking for tile images in the official API's tile service."""

    dns_count = 4

    def __init__(self):
        self.dns_index = 0

    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image.Image:
        url = f"https://tiles{self.dns_index + 1}.guildwars2.com/{continent}/{floor}/{zoom}/{x}/{y}.jpg"
        self.dns_index = (self.dns_index + 1) % self.dns_count
        response = requests.get(url)
        try:
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except HTTPError:
            return Image.new('RGB', (256, 256), 'black')

    def get_max_parallel_workers(self) -> int:
        return 32


class MapGenerator:
    def __init__(self, args):
        self.tile_source = self.get_tile_source(args)

    def generate_map_image(self, continent: int, floor: int, map_coord: MapCoordinateSystem, sector_index: int, sector_total: int) -> Image.Image:
        int_zoom_map_coord = map_coord.with_int_zoom()
        int_zoom: int = int_zoom_map_coord.zoom
        int_zoom_image_dimensions = int_zoom_map_coord.continent_to_full_image_coord(
            int_zoom_map_coord.sector_dimensions)

        image = Image.new('RGB', int_zoom_image_dimensions)

        top_left_tile = int_zoom_map_coord.continent_to_tile_coord(int_zoom_map_coord.sector_top_left)
        bottom_right_tile = int_zoom_map_coord.continent_to_tile_coord(int_zoom_map_coord.sector_bottom_right)
        top_left_image_coord = int_zoom_map_coord.continent_to_full_image_coord(int_zoom_map_coord.sector_top_left)

        tile_coords = [
            (x, y)
            for x in range(top_left_tile[0], bottom_right_tile[0] + 1)
            for y in range(top_left_tile[1], bottom_right_tile[1] + 1)
        ]

        total = len(tile_coords)
        completed = 0
        lock = threading.Lock()
        stop_event = threading.Event()

        def fetch_tile(x, y) -> tuple[Image.Image, tuple[int, int]]:
            nonlocal completed
            fetched_tile_image = self.tile_source.get_tile_image(continent, floor, int_zoom, x, y)
            fetched_position = (x * tile_image_size - top_left_image_coord[0],
                                y * tile_image_size - top_left_image_coord[1])
            with lock:
                completed += 1
            return fetched_tile_image, fetched_position

        def progress_reporter():
            time.sleep(1)
            while not stop_event.is_set():
                with lock:
                    percent = (completed / total) * 100
                    print(f"Progress: {completed}/{total} ({percent:.1f}%)")
                time.sleep(2)

        if sector_total == 1:
            print("\nGenerating map image...")
        else:
            print(f"\nGenerating map image {sector_index} / {sector_total}...")

        reporter_thread = threading.Thread(target=progress_reporter)
        reporter_thread.start()

        results = []
        max_workers = self.tile_source.get_max_parallel_workers()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(fetch_tile, x, y) for x, y in tile_coords]
            for future in as_completed(futures):
                results.append(future.result())

        stop_event.set()
        reporter_thread.join()
        print(f"Done fetching {total} tiles, combining into a single image...")

        for tile_image, position in results:
            image.paste(tile_image, position)

        if map_coord.zoom == int_zoom:
            print("Map image generated.")
            return image
        else:
            print("Resizing map image...")
            resized_image_dimensions = map_coord.continent_to_full_image_coord(map_coord.sector_dimensions)
            resized_image = image.resize(resized_image_dimensions, Resampling.LANCZOS)
            print("Map image generated.")
            return resized_image

    @staticmethod
    def get_tile_source(args) -> MapTileSource:
        match args.tiles:
            case 'local':
                return LocalMapTileSource(args.tiles_dir)
            case 'api':
                return TileApiMapTileSource()
        raise ValueError(f"Unknown tile source: {args.tiles}")
