from abc import ABC, abstractmethod

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont

from mapgen.map_coordinates import MapCoordinateSystem, zoom_factor


def get_font(size: int, bold: bool):
    if bold:
        font_url = 'assets/fonts/FiraSans/FiraSans-SemiBold.ttf'
    else:
        font_url = 'assets/fonts/FiraSans/FiraSans-Regular.ttf'
    with open(font_url, 'rb') as font_file:
        return ImageFont.truetype(font_file, size)


def get_text_zoom_multiplier(map_coord: MapCoordinateSystem):
    return ((zoom_factor + 1) / 2) ** map_coord.zoom  # increases exponentially with zoom, but slower


def get_main_label_font_size(map_coord: MapCoordinateSystem):
    return min(32, max(8, round(6 * get_text_zoom_multiplier(map_coord))))


def get_sub_label_font_size(map_coord: MapCoordinateSystem):
    return min(28, max(8, round(4.75 * get_text_zoom_multiplier(map_coord))))


class MapOverlay(ABC):
    @abstractmethod
    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        pass


class ZoneBoundaryOverlay(MapOverlay):
    category_settings = {
        'city': {'boundary_order': 0, 'label_order': 2, 'color': 'white', 'show_level': False, 'label': 'City'},
        'open_world': {'boundary_order': 0, 'label_order': 1, 'color': 'white', 'show_level': True, 'label': None},
        'guild_hall': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Guild hall'},
        'dungeon': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Dungeon'},
        'raid': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Raid'},
        'story': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Story'}
    }

    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        main_label_font = get_font(get_main_label_font_size(map_coord), True)
        sub_label_font = get_font(get_sub_label_font_size(map_coord), False)

        main_label_metrics = main_label_font.getmetrics()
        sub_label_metrics = sub_label_font.getmetrics()
        label_margin = map_coord.zoom // 2

        draw = ImageDraw.Draw(image, "RGBA")

        # Calculate and draw zone boundaries
        drawn_zones = []  # list[tuple[zone, zone_image_bounds, zone_settings]]
        zone_data.sort(key=lambda z: (ZoneBoundaryOverlay.category_settings[z['category']]['boundary_order'], z['id']))
        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            zone_image_bounds = map_coord.continent_to_sector_image_rect(continent_rect)
            settings = ZoneBoundaryOverlay.category_settings[zone['category']]
            drawn_zones.append((zone, zone_image_bounds, settings))

            draw.rectangle(zone_image_bounds, outline=settings['color'], width=1)

        # Draw zone labels
        drawn_zones.sort(key=lambda z: (ZoneBoundaryOverlay.category_settings[z[0]['category']]['label_order'], z[0]['id']))
        for zone, zone_image_bounds, settings in drawn_zones:
            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, zone_name_label_bbox[2] + 10, 2 * zone_image_bounds[1][0]),
                                max(250, 10 * zone_name_label_bbox[3] + 10, 2 * zone_image_bounds[1][1]))
            label_image = Image.new("RGBA", label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, "RGBA")

            # Find the ideal line wrapping for the zone's name and shape
            zone_image_width = zone_image_bounds[1][0] - zone_image_bounds[0][0]
            zone_image_height = zone_image_bounds[1][1] - zone_image_bounds[0][1]
            height_for_max_width = 2 * (main_label_metrics[0] + main_label_metrics[1] + label_margin) + sub_label_metrics[0] + sub_label_metrics[1]
            height_for_min_width = 1 * (main_label_metrics[0] + label_margin) + height_for_max_width
            height_diff_ratio = (zone_image_height - height_for_max_width) / (height_for_min_width - height_for_max_width)
            main_label_ideal_width = (2 - max(0, min(1, height_diff_ratio))) * zone_image_width - 8
            main_label_min_width = 4 * main_label_metrics[0]
            main_label_bounded_ideal_width = min(label_image_size[0], max(main_label_min_width, main_label_ideal_width))
            wrapped_zone_name_lines = get_wrapped_text_lines(zone['name'], main_label_font, main_label_bounded_ideal_width)

            # Draw label for the zone name
            label_pos_x = label_image.size[0] / 2
            label_pos_y = 0
            for line in wrapped_zone_name_lines:
                label_draw.text((label_pos_x, label_pos_y), line, font=main_label_font, anchor='ma', align='center', stroke_width=2, fill=settings['color'], stroke_fill='black')
                label_pos_y = label_pos_y + main_label_metrics[0] + label_margin
            label_pos_y = label_pos_y + main_label_metrics[1]

            # Draw the zone's description label (City, Dungeon etc.)
            if settings['label']:
                label_draw.text((label_pos_x, label_pos_y), settings['label'], fill=settings['color'], font=sub_label_font, anchor='ma', stroke_width=2, stroke_fill='black')
                label_pos_y = label_pos_y + sub_label_metrics[0] + sub_label_metrics[1] + label_margin

            # Draw the zone's level distribution label
            if settings['show_level']:
                level_text = str(zone['min_level']) if zone['min_level'] == zone['max_level'] else f"{zone['min_level']}–{zone['max_level']}"
                label_draw.text((label_pos_x, label_pos_y), level_text, fill=settings['color'], font=sub_label_font, anchor='ma', stroke_width=2, stroke_fill='black')

            # Paste the resulting label into the actual map image
            label_bbox = label_image.getbbox()
            label_center = (round((zone_image_bounds[0][0] + zone_image_bounds[1][0] - label_image_size[0]) / 2),
                            round((zone_image_bounds[0][1] + zone_image_bounds[1][1] - label_bbox[3] + label_bbox[1]) / 2))
            image.paste(label_image, label_center, label_image)


def get_wrapped_text_lines(text: str, font: FreeTypeFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length or len(lines[-1]) < 3:
            lines[-1] = line
        else:
            lines.append(word)
    return lines
