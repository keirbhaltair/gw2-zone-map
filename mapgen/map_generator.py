from abc import ABC, abstractmethod

from PIL import Image
from PIL.Image import Resampling

from mapgen.map_coordinates import tile_image_size, MapCoordinateSystem


class MapTileSource(ABC):
    @abstractmethod
    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image:
        pass


class LocalMapTileSource(MapTileSource):
    """Map tile source looking for tile images on the local file system, in the format of "continent/floor/zoom/x/y.jpg", for instance from that_shaman's mapgen API."""

    def __init__(self, input_directory: str):
        self.input_directory = input_directory

    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image:
        return Image.open(f"{self.input_directory}/{continent}/{floor}/{zoom}/{x}/{y}.jpg")


class MapGenerator:
    def __init__(self, tile_source: MapTileSource):
        self.tile_source = tile_source

    def generate_map_image(self, continent: int, floor: int, map_coord: MapCoordinateSystem) -> Image:
        int_zoom_map_coord = map_coord.with_int_zoom()
        int_zoom: int = int_zoom_map_coord.zoom
        int_zoom_image_dimensions = int_zoom_map_coord.continent_to_full_image_coord(int_zoom_map_coord.sector_dimensions)

        image = Image.new('RGB', int_zoom_image_dimensions)

        top_left_tile = int_zoom_map_coord.continent_to_tile_coord(int_zoom_map_coord.sector_top_left)
        bottom_right_tile = int_zoom_map_coord.continent_to_tile_coord(int_zoom_map_coord.sector_bottom_right)
        top_left_image_coord = int_zoom_map_coord.continent_to_full_image_coord(int_zoom_map_coord.sector_top_left)

        for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
            for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
                tile_image = self.tile_source.get_tile_image(continent, floor, int_zoom, x, y)
                image.paste(tile_image, (x * tile_image_size - top_left_image_coord[0], y * tile_image_size - top_left_image_coord[1]))

        if map_coord.zoom == int_zoom:
            return image
        else:
            resized_image_dimensions = map_coord.continent_to_full_image_coord(map_coord.sector_dimensions)
            return image.resize(resized_image_dimensions, Resampling.LANCZOS)
