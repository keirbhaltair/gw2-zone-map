from abc import ABC, abstractmethod
from urllib.request import urlopen

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont

from data.portals import portals
from mapgen.map_coordinates import MapCoordinateSystem, zoom_factor


def get_font(size: int, bold: bool):
    if bold:
        font_url = 'assets/fonts/FiraSans/FiraSans-SemiBold.ttf'
    else:
        font_url = 'assets/fonts/FiraSans/FiraSans-Regular.ttf'
    with open(font_url, 'rb') as font_file:
        return ImageFont.truetype(font_file, size)


def get_zoom_size_multiplier(map_coord: MapCoordinateSystem):
    return ((zoom_factor + 1) / 2) ** map_coord.zoom  # increases exponentially with zoom, but slower


def get_main_label_font_size(map_coord: MapCoordinateSystem):
    return min(32, max(8, round(6 * get_zoom_size_multiplier(map_coord))))


def get_sub_label_font_size(map_coord: MapCoordinateSystem):
    return min(28, max(8, round(4.75 * get_zoom_size_multiplier(map_coord))))


def get_icon_size(map_coord: MapCoordinateSystem):
    return min(32, max(12, round(7 * get_zoom_size_multiplier(map_coord))))


class MapOverlay(ABC):
    @abstractmethod
    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        pass


class ZoneMapOverlay(MapOverlay):
    category_settings = {
        'city': {'boundary_order': 0, 'label_order': 2, 'color': 'white', 'show_level': False, 'label': 'City'},
        'open_world': {'boundary_order': 0, 'label_order': 1, 'color': 'white', 'show_level': True, 'label': None},
        'guild_hall': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Guild hall'},
        'dungeon': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Dungeon'},
        'raid': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Raid'},
        'story': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': 'Story'},
        'misc': {'boundary_order': 1, 'label_order': 0, 'color': (255, 160, 0), 'show_level': False, 'label': None},
    }

    portals = {
        'neighbor': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/a/ae/Asura_gate_starter_area_%28map_icon%29.png")), 'line_color': (45, 185, 227, 150)},
        'asura_gate': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/6/6c/Asura_gate_%28map_icon%29.png")), 'line_color': None},
        'dungeon': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/3/3c/Dungeon_%28map_icon%29.png")), 'line_color': None},
        'raid': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/8/86/Raid_%28map_icon%29.png")), 'line_color': (199, 76, 42, 150)},
        'fractal': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/9/9f/Fractals_of_the_Mists_%28map_icon%29.png")), 'line_color': None},
        'strike': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/e/e7/Strike_Mission_%28map_icon%29.png")), 'line_color': None},
    }

    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem):
        main_label_font = get_font(get_main_label_font_size(map_coord), True)
        sub_label_font = get_font(get_sub_label_font_size(map_coord), False)
        icon_size = get_icon_size(map_coord)

        main_label_metrics = main_label_font.getmetrics()
        sub_label_metrics = sub_label_font.getmetrics()
        label_margin = map_coord.zoom // 2

        draw = ImageDraw.Draw(image, 'RGBA')

        # Draw zone boundaries
        drawn_zones = []  # list[tuple[zone, zone_image_bounds, zone_settings]]
        zone_data.sort(key=lambda z: (ZoneMapOverlay.category_settings[z['category']]['boundary_order'], z['id']))
        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            zone_image_bounds = map_coord.continent_to_sector_image_rect(continent_rect)
            settings = ZoneMapOverlay.category_settings[zone['category']]
            drawn_zones.append((zone, zone_image_bounds, settings))

            draw.rectangle(zone_image_bounds, outline=settings['color'], width=1)

        # Draw icons for portals, asura gates, dungeons etc.
        for portal_type in reversed(portals.keys()):
            portal_icon = self.get_portal_icon(portal_type, icon_size)
            for portal in portals[portal_type]:
                portal_image_coord = map_coord.continent_to_sector_image_coord((portal[0], portal[1]))
                portal_paste_coord = (round(portal_image_coord[0] - portal_icon.size[0] / 2), round(portal_image_coord[1] - portal_icon.size[1] / 2))
                if len(portal) == 4:
                    portal2_image_coord = map_coord.continent_to_sector_image_coord((portal[2], portal[3]))
                    portal2_paste_coord = (round(portal2_image_coord[0] - portal_icon.size[0] / 2), round(portal2_image_coord[1] - portal_icon.size[1] / 2))
                    self.draw_portal_connection_line(image, portal_image_coord, portal2_image_coord, portal_type)
                    image.paste(portal_icon, portal2_paste_coord, portal_icon)
                image.paste(portal_icon, portal_paste_coord, portal_icon)

        # Draw zone labels
        drawn_zones.sort(key=lambda z: (ZoneMapOverlay.category_settings[z[0]['category']]['label_order'], z[0]['id']))
        for zone, zone_image_bounds, settings in drawn_zones:
            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, zone_name_label_bbox[2] + 10, 2 * zone_image_bounds[1][0]),
                                max(250, 10 * zone_name_label_bbox[3] + 10, 2 * zone_image_bounds[1][1]))
            label_image = Image.new('RGBA', label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, 'RGBA')

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

    @staticmethod
    def get_portal_icon(portal_type, icon_size):
        if '/' not in portal_type:
            template_icon = ZoneMapOverlay.portals[portal_type]['icon']
            return template_icon.resize((icon_size, icon_size), resample=Image.LANCZOS)
        else:
            # Blend multiple icons together so that they're all at least partially visible despite overlapping
            blended_icon = Image.new('RGBA', (icon_size, icon_size), color=(255, 255, 255, 0))
            portal_types = portal_type.split('/')
            arc_angle = 360 / len(portal_types)
            for i, t in enumerate(portal_types):
                template_icon = ZoneMapOverlay.portals[t]['icon']
                resized_icon = template_icon.resize((icon_size, icon_size), resample=Image.LANCZOS)
                start_angle = i * arc_angle - 90
                end_angle = (i + 1) * arc_angle - 90
                mask = Image.new('L', (icon_size, icon_size), color='white')
                ImageDraw.Draw(mask).pieslice(((0, 0), (icon_size, icon_size)), start_angle, end_angle, width=0, fill='black')
                blended_icon = Image.composite(blended_icon, resized_icon, mask)
            return blended_icon

    @staticmethod
    def draw_portal_connection_line(map_image, portal1_image_coord, portal2_image_coord, portal_type):
        """Draws the line between two connected far-away portals, with super-sampling for simple, if inefficient, antialiasing."""
        margin = 2
        super_sampling_factor = 4
        line_rect = abs(portal1_image_coord[0] - portal2_image_coord[0]), abs(portal1_image_coord[1] - portal2_image_coord[1])
        paste_coord = min(portal1_image_coord[0], portal2_image_coord[0]) - margin, min(portal1_image_coord[1], portal2_image_coord[1]) - margin
        super_sampled_image_size = super_sampling_factor * (line_rect[0] + margin), super_sampling_factor * (line_rect[1] + margin)
        super_sampled_image = Image.new('RGBA', super_sampled_image_size)
        super_sampled_draw = ImageDraw.Draw(super_sampled_image)

        line_color = ZoneMapOverlay.portals[portal_type]['line_color']
        line_coord = ((super_sampling_factor * (portal1_image_coord[0] - paste_coord[0]), super_sampling_factor * (portal1_image_coord[1] - paste_coord[1])),
                      (super_sampling_factor * (portal2_image_coord[0] - paste_coord[0]), super_sampling_factor * (portal2_image_coord[1] - paste_coord[1])))
        super_sampled_draw.line(line_coord, fill=line_color, width=2 * super_sampling_factor)

        resized_size = line_rect[0] + margin, line_rect[1] + margin
        smooth_line_image = super_sampled_image.resize(resized_size, resample=Image.LANCZOS)
        map_image.paste(smooth_line_image, paste_coord, smooth_line_image)


def get_wrapped_text_lines(text: str, font: FreeTypeFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length or len(lines[-1]) < 3:
            lines[-1] = line
        else:
            lines.append(word)
    return lines
