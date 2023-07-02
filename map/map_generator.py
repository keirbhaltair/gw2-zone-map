from abc import ABC, abstractmethod

from PIL import Image

from data.continents import MapParameters


class MapTileSource(ABC):
    @abstractmethod
    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image:
        pass


class LocalMapTileSource(MapTileSource):
    """Map tile source looking for tile images on the local file system, in the format of "continent/floor/zoom/x/y.jpg", for instance from that_shaman's map API."""

    def __init__(self, input_directory: str):
        self.input_directory = input_directory

    def get_tile_image(self, continent: int, floor: int, zoom: int, x: int, y: int) -> Image:
        return Image.open(f"{self.input_directory}/{continent}/{floor}/{zoom}/{x}/{y}.jpg")


class MapGenerator:
    def __init__(self, map_params: MapParameters, tile_source: MapTileSource):
        self.map_params = map_params
        self.tile_source = tile_source

    def generate_map_image(self, continent: int, floor: int, zoom: int) -> Image:
        self.map_params.check_zoom(zoom)
        tile_dimensions = self.map_params.get_tile_count(zoom)
        map_image_dimensions = (tile_dimensions[0] * self.map_params.tile_image_size, tile_dimensions[1] * self.map_params.tile_image_size)
        map_image = Image.new("RGB", map_image_dimensions)

        for x in range(tile_dimensions[0]):
            for y in range(tile_dimensions[1]):
                tile_image = self.tile_source.get_tile_image(continent, floor, zoom, x, y)
                map_image.paste(tile_image, (x * self.map_params.tile_image_size, y * self.map_params.tile_image_size))

        return map_image
