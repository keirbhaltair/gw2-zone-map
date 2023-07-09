import math
from dataclasses import dataclass

tile_image_size = 256
zoom_factor = 2


@dataclass
class MapParameters:
    continent_id: int
    dimensions: tuple[int, int]
    min_zoom: int
    max_zoom: int
    max_zoom_tile_dimensions: int = tile_image_size


@dataclass
class MapSector:
    continent_id: int
    continent_rect: tuple[tuple[int, int], tuple[int, int]] | None

    def width(self):
        return self.continent_rect[1][0] - self.continent_rect[0][0]

    def height(self):
        return self.continent_rect[1][1] - self.continent_rect[0][1]


@dataclass
class MapLayout:
    parts: list[tuple[tuple[int, int], MapSector]]

    @classmethod
    def single_sector(cls, sector: MapSector):
        return cls([((0, 0), sector)])


class MapCoordinateSystem:
    def __init__(self, map_params: MapParameters, zoom: int, sector: MapSector = None):
        if zoom < map_params.min_zoom or zoom > map_params.max_zoom:
            raise ValueError(f"Zoom must be in the interval [{map_params.min_zoom}, {map_params.max_zoom}]")

        full_dim_rect = ((0, 0), (map_params.dimensions[0] - 1, map_params.dimensions[1] - 1))
        sector_rect = full_dim_rect if sector is None or sector.continent_rect is None else sector.continent_rect
        if sector_rect[0][0] < full_dim_rect[0][0] or sector_rect[0][1] < full_dim_rect[0][1] or sector_rect[1][0] > full_dim_rect[1][0] or sector_rect[1][1] > full_dim_rect[1][1]:
            raise ValueError(f"Sector {sector} must be within bounds {full_dim_rect}.")
        elif sector_rect[0][0] >= sector_rect[1][0] or sector_rect[0][1] >= sector_rect[1][1]:
            raise ValueError(f"Sector {sector} must be defined as (top, left, bottom, right).")

        self.map_params = map_params
        self.zoom = zoom

        self.tile_dimensions = (zoom_factor ** (map_params.max_zoom - zoom)) * map_params.max_zoom_tile_dimensions
        self.continent_to_tile_multiplier = 1 / self.tile_dimensions
        self.continent_to_image_multiplier = tile_image_size * self.continent_to_tile_multiplier
        self.sector_dimensions = (sector_rect[1][0] - sector_rect[0][0] + 1, sector_rect[1][1] - sector_rect[0][1] + 1)
        self.sector_top_left = sector_rect[0][0], sector_rect[0][1]
        self.sector_bottom_right = sector_rect[1][0], sector_rect[1][1]

    def continent_to_tile_coord(self, continent_coord: (int, int)) -> (int, int):
        return (math.floor(self.continent_to_tile_multiplier * continent_coord[0]),
                math.floor(self.continent_to_tile_multiplier * continent_coord[1]))

    def continent_to_full_image_coord(self, continent_coord: (int, int)) -> (int, int):
        return (math.floor(self.continent_to_image_multiplier * continent_coord[0]),
                math.floor(self.continent_to_image_multiplier * continent_coord[1]))

    def continent_to_sector_image_coord(self, continent_coord: (int, int)) -> (int, int):
        return (math.floor(self.continent_to_image_multiplier * (continent_coord[0] - self.sector_top_left[0])),
                math.floor(self.continent_to_image_multiplier * (continent_coord[1] - self.sector_top_left[1])))

    def continent_to_sector_image_rect(self, continent_rect: ((int, int), (int, int))) -> ((int, int), (int, int)):
        return (self.continent_to_sector_image_coord(continent_rect[0]),
                self.continent_to_sector_image_coord(continent_rect[1]))

    def is_point_contained_in_sector(self, continent_coord: (int, int)) -> bool:
        return self.sector_top_left[0] < continent_coord[0] < self.sector_bottom_right[0] and self.sector_top_left[1] < continent_coord[1] < self.sector_bottom_right[1]

    def is_rect_contained_in_sector(self, continent_rect: ((int, int), (int, int))) -> bool:
        return self.is_point_contained_in_sector(continent_rect[0]) and self.is_point_contained_in_sector(continent_rect[1])
