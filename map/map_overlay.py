from abc import ABC, abstractmethod

from PIL import Image, ImageFont, ImageDraw

from data.continents import MapParameters
from data.zones import ZoneData


class MapOverlay(ABC):
    @abstractmethod
    def draw_overlay(self, image: Image, map_params: MapParameters, zoom: int, zone_data: list[ZoneData]):
        pass


class ZoneBoundaryOverlay(MapOverlay):
    def draw_overlay(self, image: Image, map_params: MapParameters, zoom: int, zone_data: list[ZoneData]):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 16)

        tile_coord_size = map_params.tile_coord_size_min_zoom * (map_params.zoom_factor ** (zoom - map_params.min_zoom))
        tile_coord_multiplier = map_params.tile_image_size / tile_coord_size

        for zone in zone_data:
            rect = zone.continent_rect
            image_rect = (rect[0][0] * tile_coord_multiplier, rect[0][1] * tile_coord_multiplier, rect[1][0] * tile_coord_multiplier, rect[1][1] * tile_coord_multiplier)
            draw.rectangle(image_rect, outline='white', width=1)

            image_rect_center = ((image_rect[0] + image_rect[2]) / 2, (image_rect[1] + image_rect[3]) / 2)
            draw.text(image_rect_center, zone.name, fill='white', font=font, anchor='mm')
