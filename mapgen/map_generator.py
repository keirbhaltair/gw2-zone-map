import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

import requests
from PIL import Image
from PIL.Image import Resampling
from requests import HTTPError

from data.map_images import tile_api_map_overlays
from mapgen.map_coordinates import tile_image_size, MapCoordinateSystem


class MapTileSource(ABC):
    @abstractmethod
    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image.Image:
        pass

    @abstractmethod
    def get_max_parallel_workers(self) -> int:
        pass

    def get_image_overlays(self, continent: int, floor: int) -> list[
        tuple[Image.Image, tuple[tuple[int, int], tuple[int, int]]]]:
        """
        Returns a list of tuples: (overlay_image, continent_rect)
        where continent_rect is ((min_x, min_y), (max_x, max_y)).
        """
        return []


class LocalMapTileSource(MapTileSource):
    """Map tile source looking for tile images on local file system."""

    def __init__(self, input_directory: str):
        self.input_directory = input_directory

    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image.Image:
        return Image.open(f"{self.input_directory}/{continent}/{floor}/{zoom}/{x}/{y}.jpg")

    def get_max_parallel_workers(self) -> int:
        return 1


class TileApiMapTileSource(MapTileSource):
    """Map tile source looking for tile images in official API's tile service."""

    dns_count = 4

    def __init__(self):
        self.dns_index = 0
        self._overlay_cache: dict[str, Image.Image] = {}

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

    def get_image_overlays(self, continent: int, floor: int) -> list[
        tuple[Image.Image, tuple[tuple[int, int], tuple[int, int]]]]:
        overlays = []
        for ov in tile_api_map_overlays:
            if "continent_id" in ov and ov["continent_id"] != continent:
                continue

            url = ov["image_url"]
            if url not in self._overlay_cache:
                try:
                    res = requests.get(url)
                    res.raise_for_status()
                    # Convert to RGBA to preserve WebP transparency during alpha compositing
                    self._overlay_cache[url] = Image.open(BytesIO(res.content)).convert("RGBA")
                except Exception as e:
                    print(f"Warning: Failed to download overlay {url}: {e}")
                    continue

            overlay_img = self._overlay_cache[url]
            overlays.append((overlay_img, ov["continent_rect"]))

        return overlays


class MapGenerator:
    def __init__(self, args):
        self.tile_source = self.get_tile_source(args)

    def generate_map_image(self, continent: int, floor: int, map_coord: MapCoordinateSystem, sector_index: int,
                           sector_total: int) -> Image.Image:
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

        # 1. Base tile composition
        for tile_image, position in results:
            image.paste(tile_image, position)

        # 2. Apply Image Overlays
        overlays = self.tile_source.get_image_overlays(continent, floor)
        if overlays:
            print("Applying image overlays...")
            canvas_w, canvas_h = image.size

            for overlay_img, (ov_top_left, ov_bottom_right) in overlays:
                # Map continent rect to target pixel coordinates at current integer zoom
                px_top_left = int_zoom_map_coord.continent_to_full_image_coord(ov_top_left)
                px_bottom_right = int_zoom_map_coord.continent_to_full_image_coord(ov_bottom_right)

                # Relative placement on the sector canvas
                canvas_x1 = px_top_left[0] - top_left_image_coord[0]
                canvas_y1 = px_top_left[1] - top_left_image_coord[1]
                canvas_x2 = px_bottom_right[0] - top_left_image_coord[0]
                canvas_y2 = px_bottom_right[1] - top_left_image_coord[1]

                ov_width = canvas_x2 - canvas_x1
                ov_height = canvas_y2 - canvas_y1

                # Skip if the overlay falls completely outside the rendered sector
                if canvas_x2 <= 0 or canvas_y2 <= 0 or canvas_x1 >= canvas_w or canvas_y1 >= canvas_h:
                    continue

                # Scale overlay to match the current zoom scale
                resized_overlay = overlay_img.resize((ov_width, ov_height), Resampling.LANCZOS)

                # Crop overlay edges if partially off-canvas
                crop_x1 = max(0, -canvas_x1)
                crop_y1 = max(0, -canvas_y1)
                crop_x2 = ov_width - max(0, canvas_x2 - canvas_w)
                crop_y2 = ov_height - max(0, canvas_y2 - canvas_h)

                visible_overlay = resized_overlay.crop((crop_x1, crop_y1, crop_x2, crop_y2))

                paste_x = max(0, canvas_x1)
                paste_y = max(0, canvas_y1)

                # Paste onto base canvas using alpha transparency mask
                image.paste(visible_overlay, (paste_x, paste_y), visible_overlay)

        # 3. Handle floating point zoom resizing
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
