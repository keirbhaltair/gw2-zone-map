import math

from mapgen.overlay.overlay_util import *


class MasteryRegionMapOverlay(MapOverlay):
    base_text_color = (255, 255, 255, 255)
    sub_text_color = (255, 255, 255, 255)
    debug_color = (255, 0, 195, 255)

    mastery_settings = {
        'Central Tyria': {'color': (240, 51, 7, 160)},
        'Heart of Thorns': {'color': (0, 255, 92, 160)},
        'Path of Fire': {'color': (202, 5, 237, 160)},
        'Icebrood Saga': {'color': (20, 153, 255, 160)},
        'End of Dragons': {'color': (10, 240, 221, 160)},
        'Secrets of the Obscure': {'color': (255, 207, 13, 160)},
        'Janthir Wilds': {'color': (28, 44, 116, 160)},
        'Visions of Eternity': {'color': (235, 118, 9, 160)},
    }

    category_settings = {
        'city': {'order': 1, 'label_size': 1},
        'lobby': {'order': 1, 'label_size': 1},
        'outpost': {'order': 1, 'label_size': 1},
        'open_world': {'order': 0, 'label_size': 1},
        'festival': {'order': 1, 'label_size': 0.8},
        'homestead': {'order': 1, 'label_size': 0.8},
        'guild_hall': {'order': 1, 'label_size': 0.8},
        'dungeon': {'order': 3, 'label_size': 0.8},
        'raid': {'order': 3, 'label_size': 0.8},
        'raid_convergence': {'order': 3, 'label_size': 0.8},
        'strike': {'order': 3, 'label_size': 0.75},
        'story': {'order': 0, 'label_size': 0.8},
        'public_instance': {'order': 2, 'label_size': 0.8},
        'lounge': {'order': 0, 'label_size': 0.75},
        'misc': {'order': 1, 'label_size': 0.75},
    }

    def draw_overlay(self, image: Image.Image, zone_data: list[dict], map_layout: MapLayout, map_coord: MapCoordinateSystem,
                     scale_factor: float, debug: bool):
        draw = ImageDraw.Draw(image, 'RGBA')

        # Draw zone boundaries
        zone_data.sort(key=lambda z: (self.category_settings[z['category']]['order'], z['id']))
        drawn_zones = []  # list[tuple[zone, zone_image_bounds, zone_settings]]
        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if zone['id'] in map_layout.zone_blacklist or not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            zone_image_rect = map_coord.continent_to_sector_image_rect(continent_rect)
            line_width = get_line_width(map_coord, scale_factor)
            outline_rect = ((zone_image_rect[0][0] - math.floor((line_width - 1) / 2), zone_image_rect[0][1] - math.floor((line_width - 1) / 2)),
                            (zone_image_rect[1][0] + math.floor(line_width / 2), zone_image_rect[1][1] + math.floor(line_width / 2)))

            bg_color = self.mastery_settings[zone['mastery_region']]['color']
            draw.rectangle(outline_rect, outline='white', width=get_line_width(map_coord, scale_factor), fill=bg_color)
            settings = self.category_settings[zone['category']]

            drawn_zones.append((zone, zone_image_rect, settings))

        for zone, zone_image_rect, settings in drawn_zones:
            # Choose the fonts to draw the labels with
            label_size_multiplier = scale_factor * (zone['label_size'] if 'label_size' in zone else settings['label_size'])
            main_label_font_size = get_main_label_font_size(map_coord, 1 * label_size_multiplier)
            main_label_font = get_font(main_label_font_size, True, False)
            main_label_line_margin = main_label_font_size // 8
            main_label_outline_width = get_text_outline_width(main_label_font_size)
            mastery_region_font_size = get_sub_label_font_size(map_coord, 1 * label_size_multiplier)
            mastery_region_font = get_font(mastery_region_font_size, False, True)
            mastery_region_margin = mastery_region_font_size // 8
            mastery_region_outline_width = get_text_outline_width(mastery_region_font_size)

            # Choose the location and alignment where we want to display the zone's label (center of the zone boundary unless overridden)
            label_anchor, label_image_rect = get_zone_pos(map_coord, zone, zone_image_rect)

            if debug:
                draw.rectangle(label_image_rect, outline=self.debug_color, width=1)

            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, round(zone_name_label_bbox[2] + 10), round(2 * label_image_rect[1][0] + 20)),
                                max(250, round(10 * zone_name_label_bbox[3] + 10), round(2 * label_image_rect[1][1] + 20)))
            label_image = Image.new('RGBA', label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, 'RGBA')
            label_draw_text_anchor = label_anchor[0] + 'a'

            # Collect all lines to draw so that they can be drawn in reverse order to keep earlier lines on top
            lines_to_draw = []

            # Find the ideal line wrapping for the zone's name and shape
            wrapped_zone_name_lines = wrap_label(zone['name'], main_label_font, main_label_line_margin, label_image_rect, label_image_size, map_coord, scale_factor)

            # Draw label for the zone name
            label_pos_x = round(label_image_size[0] / 2) if label_anchor[0] == 'm' else 2 if label_anchor[0] == 'l' else label_image_size[0] - 2
            label_pos_y = 0
            for line in wrapped_zone_name_lines:
                lines_to_draw.append((line, label_pos_y, main_label_font, main_label_outline_width, self.base_text_color))
                label_pos_y = label_pos_y + main_label_font.getmetrics()[0] + main_label_line_margin
            label_pos_y = label_pos_y + max(0, main_label_font.getmetrics()[1] - main_label_line_margin)

            # Draw the mastery region
            wrapped_mastery_region_lines = wrap_label(zone['mastery_region'], mastery_region_font, mastery_region_margin, label_image_rect, label_image_size, map_coord,
                                                      scale_factor, 1.25)
            for line in wrapped_mastery_region_lines:
                lines_to_draw.append((line, label_pos_y, mastery_region_font, mastery_region_outline_width, self.sub_text_color))
                label_pos_y = label_pos_y + mastery_region_font.getmetrics()[0] + mastery_region_margin

            # Perform the actual draws
            for (line, pos_y, font, outline_width, color) in reversed(lines_to_draw):
                label_draw.text((label_pos_x, pos_y), line, font=font, anchor=label_draw_text_anchor, align='center', stroke_width=outline_width, fill=color, stroke_fill='black')

            # Paste the resulting label into the actual map image
            label_paste_pos = calculate_zone_label_paste_position(label_anchor, label_image, label_image_rect)
            image.paste(label_image, label_paste_pos, label_image)

    def draw_legend(self, image: Image.Image, map_layout: MapLayout, map_coord: MapCoordinateSystem, scale_factor: float):
        draw_title('Mastery regions', image, map_coord, map_layout, scale_factor)
