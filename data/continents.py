from dataclasses import dataclass


@dataclass
class MapParameters:
    tile_coord_size_min_zoom: int
    tile_dimensions_min_zoom: (int, int)
    min_zoom: int
    max_zoom: int

    tile_image_size: int = 256
    zoom_factor: float = 1 / 2

    def full_coord_size(self):
        return tuple(map(lambda dim: dim * self.tile_coord_size_min_zoom, self.tile_dimensions_min_zoom))

    def get_tile_count(self, zoom: int):
        self.check_zoom(zoom)
        return tuple(map(lambda dim: dim * (2 ** (zoom - self.min_zoom)), self.tile_dimensions_min_zoom))

    def check_zoom(self, zoom):
        if zoom < self.min_zoom or zoom > self.max_zoom:
            raise ValueError(f"Zoom must be in the interval [{self.min_zoom}, {self.max_zoom}]")


continent_map_params: dict[int, MapParameters] = {
    1: MapParameters(2 ** 14, (5, 7), 1, 7)
}
