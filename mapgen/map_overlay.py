from abc import ABC, abstractmethod
from urllib.request import urlopen

from PIL import Image, ImageFont, ImageDraw

from mapgen.map_coordinates import MapCoordinateSystem

font_regular_url = "https://d1h9a8s8eodvjz.cloudfront.net/fonts/menomonia/08-02-12/font/menomonia.ttf"
font_italic_url = "https://d1h9a8s8eodvjz.cloudfront.net/fonts/menomonia/08-02-12/font/menomonia-italic.ttf"


class MapOverlay(ABC):
    @abstractmethod
    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        pass


class ZoneBoundaryOverlay(MapOverlay):
    category_settings = {
        'city': {'order': 0, 'color': 'white', 'show_level': False, 'label': 'City'},
        'open_world': {'order': 0, 'color': 'white', 'show_level': True, 'label': None},
        'guild_hall': {'order': 2, 'color': (255, 160, 0), 'show_level': False, 'label': 'Guild hall'},
        'dungeon': {'order': 1, 'color': (255, 160, 0), 'show_level': False, 'label': 'Dungeon'},
        'raid': {'order': 1, 'color': (255, 160, 0), 'show_level': False, 'label': 'Raid'},
        'story': {'order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Story'}
    }

    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        label_multiline_offset = 22
        zone_name_font = ImageFont.truetype(urlopen(font_regular_url), 20)
        label_font = ImageFont.truetype(urlopen(font_italic_url), 16)

        draw = ImageDraw.Draw(image)

        zone_data.sort(key=lambda z: (ZoneBoundaryOverlay.category_settings[z['category']]['order'], z['id']))

        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            category = zone['category']
            settings = ZoneBoundaryOverlay.category_settings[category]

            image_rect = map_coord.continent_to_sector_image_rect(continent_rect)
            draw.rectangle(image_rect, outline=settings['color'], width=1)

            text_y_offset = 0
            if settings['label']:
                text_y_offset = text_y_offset - 0.5 * label_multiline_offset
            if settings['show_level']:
                text_y_offset = text_y_offset - 0.5 * label_multiline_offset

            text_center = ((image_rect[0][0] + image_rect[1][0]) / 2, (image_rect[0][1] + image_rect[1][1]) / 2 + text_y_offset)
            draw.text(text_center, zone['name'], fill=settings['color'], font=zone_name_font, anchor='mm', stroke_width=1, stroke_fill='black')

            if settings['label']:
                text_center = (text_center[0], text_center[1] + label_multiline_offset)
                draw.text(text_center, settings['label'], fill=settings['color'], font=label_font, anchor='mm', stroke_width=1, stroke_fill='black')

            if settings['show_level']:
                text_center = (text_center[0], text_center[1] + label_multiline_offset)
                level_text = str(zone['min_level']) if zone['min_level'] == zone['max_level'] else f"{zone['min_level']}–{zone['max_level']}"
                draw.text(text_center, level_text, fill=settings['color'], font=label_font, anchor='mm', stroke_width=1, stroke_fill='black')
