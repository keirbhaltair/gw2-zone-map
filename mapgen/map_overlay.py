import math
from abc import ABC, abstractmethod
from functools import cache
from urllib.request import urlopen

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont

from data.portals import portals
from mapgen.map_coordinates import MapCoordinateSystem, zoom_factor, MapLayout


@cache
def get_font(size: int, bold: bool):
    if bold:
        font_url = 'assets/fonts/FiraSans/FiraSans-SemiBold.ttf'
    else:
        font_url = 'assets/fonts/FiraSans/FiraSans-Regular.ttf'
    with open(font_url, 'rb') as font_file:
        return ImageFont.truetype(font_file, size)


@cache
def get_zoom_size_multiplier(map_coord: MapCoordinateSystem, size_multiplier):
    return size_multiplier * (zoom_factor ** map_coord.zoom)


@cache
def get_main_label_font_size(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(32, max(8, round(2.5 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_sub_label_font_size(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(28, max(8, round(2 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_legend_font_size(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(28, max(10, round(2 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_icon_size(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(32, max(12, round(3 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_line_width(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(32, max(1, round(0.3 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_text_outline_width(map_coord: MapCoordinateSystem, size_multiplier: int = 1):
    return min(8, max(1, round(0.3 * get_zoom_size_multiplier(map_coord, size_multiplier))))


def get_wrapped_text_lines(text: str, font: FreeTypeFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length or len(lines[-1]) < 3:
            lines[-1] = line
        else:
            lines.append(word)
    return lines


def wrap_zone_name(label_image_rect, label_image_size, label_margin, main_label_font, main_label_metrics, zone, map_coord, scale_factor):
    if '\n' in zone['name']:
        return zone['name'].split('\n')
    label_box_image_width = label_image_rect[1][0] - label_image_rect[0][0]
    label_box_image_height = label_image_rect[1][1] - label_image_rect[0][1]
    height_for_max_width = 2.75 * (sum(main_label_metrics) + label_margin)
    height_for_min_width = 1 * (main_label_metrics[0] + label_margin) + height_for_max_width
    height_diff_ratio = (label_box_image_height - height_for_max_width) / (height_for_min_width - height_for_max_width)
    main_label_ideal_width = (2 - max(0, min(1, height_diff_ratio))) * label_box_image_width - get_zoom_size_multiplier(map_coord, scale_factor)
    main_label_min_width = 4 * main_label_metrics[0]
    main_label_bounded_ideal_width = min(label_image_size[0], max(main_label_min_width, main_label_ideal_width))
    wrapped_zone_name_lines = get_wrapped_text_lines(zone['name'], main_label_font, main_label_bounded_ideal_width)
    return wrapped_zone_name_lines


def calculate_zone_label_paste_position(label_anchor, label_image: Image, label_image_rect: tuple[tuple[float, float], tuple[float, float]]):
    label_bbox = label_image.getbbox()
    label_paste_pos = []
    match label_anchor[0]:
        case 'l':
            label_paste_pos.append(label_image_rect[0][0])
        case 'm':
            label_paste_pos.append(round((label_image_rect[0][0] + label_image_rect[1][0] - label_image.size[0]) / 2))
        case 'r':
            label_paste_pos.append(label_image_rect[1][0] - label_image.size[0])
    match label_anchor[1]:
        case 't':
            label_paste_pos.append(label_image_rect[0][1])
        case 'm':
            label_paste_pos.append(round((label_image_rect[0][1] + label_image_rect[1][1] - label_bbox[3] + label_bbox[1]) / 2))
        case 'b':
            label_paste_pos.append(label_image_rect[1][1] - label_bbox[3] + label_bbox[1] - 4)
    return label_paste_pos


def calculate_legend_paste_position(image: Image, legend_size: tuple[int, int], map_layout: MapLayout):
    coord = []
    match map_layout.legend_align[0]:
        case 'l':
            coord.append(map_layout.legend_image_coord[0])
        case 'r':
            coord.append(image.size[0] - map_layout.legend_image_coord[0] - legend_size[0])
    match map_layout.legend_align[1]:
        case 't':
            coord.append(map_layout.legend_image_coord[1])
        case 'b':
            coord.append(image.size[1] - map_layout.legend_image_coord[1] - legend_size[1])
    return coord[0], coord[1], coord[0] + legend_size[0], coord[1] + legend_size[1]


class MapOverlay(ABC):
    @abstractmethod
    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem, scale_factor: float):
        pass

    @abstractmethod
    def draw_legend(self, image: Image, map_layout: MapLayout, map_coord: MapCoordinateSystem, scale_factor: float):
        pass


class NoMapOverlay(MapOverlay):
    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem, scale_factor: float):
        pass

    def draw_legend(self, image: Image, map_layout: MapLayout, map_coord: MapCoordinateSystem, scale_factor: float):
        pass


class ZoneMapOverlay(MapOverlay):
    base_line_color = (255, 255, 255, 255)
    special_line_color = (255, 160, 15, 255)

    category_settings = {
        'city': {'boundary_order': 0, 'label_order': 2, 'special': False, 'show_level': False, 'label': 'City'},
        'lobby': {'boundary_order': 0, 'label_order': 2, 'special': False, 'show_level': False, 'label': 'Lobby'},
        'open_world': {'boundary_order': 0, 'label_order': 1, 'special': False, 'show_level': True, 'label': None},
        'festival': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Festival zone'},
        'guild_hall': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Guild hall'},
        'dungeon': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Dungeon'},
        'raid': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Raid'},
        'strike': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Strike mission'},
        'story': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Story'},
        'hybrid_instance': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': 'Boss instance'},
        'lounge': {'boundary_order': 0, 'label_order': 0, 'special': False, 'show_level': False, 'label': 'Lounge'},
        'misc': {'boundary_order': 1, 'label_order': 0, 'special': True, 'show_level': False, 'label': None},
    }

    portal_settings = {
        'neighbor': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/a/ae/Asura_gate_starter_area_%28map_icon%29.png")), 'line_color': (45, 185, 227, 150),
                     'legend': 'Zone portal'},
        'asura_gate': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/6/6c/Asura_gate_%28map_icon%29.png")), 'line_color': None,
                       'legend': 'Asura gate'},
        'dungeon': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/3/3c/Dungeon_%28map_icon%29.png")), 'line_color': None,
                    'legend': 'Dungeon'},
        'fractal': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/9/9f/Fractals_of_the_Mists_%28map_icon%29.png")), 'line_color': None,
                    'legend': 'Fractals of the Mists'},
        'strike': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/e/e7/Strike_Mission_%28map_icon%29.png")), 'line_color': None,
                   'legend': 'Strike mission'},
        'raid': {'icon': Image.open(urlopen("https://wiki.guildwars2.com/images/8/86/Raid_%28map_icon%29.png")), 'line_color': (199, 76, 42, 150),
                 'legend': 'Raid'},
    }

    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem, scale_factor: float):
        draw = ImageDraw.Draw(image, 'RGBA')

        # Draw zone boundaries
        drawn_zones = []  # list[tuple[zone, zone_image_bounds, zone_settings]]
        zone_data.sort(key=lambda z: (self.category_settings[z['category']]['boundary_order'], z['id']))
        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            zone_image_rect = map_coord.continent_to_sector_image_rect(continent_rect)
            line_width = get_line_width(map_coord, scale_factor)
            outline_rect = ((zone_image_rect[0][0] - math.floor((line_width - 1) / 2), zone_image_rect[0][1] - math.floor((line_width - 1) / 2)),
                            (zone_image_rect[1][0] + math.floor(line_width / 2), zone_image_rect[1][1] + math.floor(line_width / 2)))

            settings = self.category_settings[zone['category']]
            line_color = self.special_line_color if settings['special'] else self.base_line_color

            drawn_zones.append((zone, zone_image_rect, settings))

            draw.rectangle(outline_rect, outline=line_color, width=line_width)

        # Draw icons for portals, asura gates, dungeons etc.
        icon_size = get_icon_size(map_coord, scale_factor)
        for portal_type in reversed(portals.keys()):
            portal_icon = self.get_portal_icon(portal_type, icon_size)
            for portal in portals[portal_type]:
                portal_image_coord = map_coord.continent_to_sector_image_coord((portal[0], portal[1]))
                portal_paste_coord = (round(portal_image_coord[0] - portal_icon.size[0] / 2), round(portal_image_coord[1] - portal_icon.size[1] / 2))
                if len(portal) == 4:
                    portal2_image_coord = map_coord.continent_to_sector_image_coord((portal[2], portal[3]))
                    portal2_paste_coord = (round(portal2_image_coord[0] - portal_icon.size[0] / 2), round(portal2_image_coord[1] - portal_icon.size[1] / 2))
                    self.draw_portal_connection_line(image, portal_image_coord, portal2_image_coord, portal_type, map_coord, scale_factor)
                    image.paste(portal_icon, portal2_paste_coord, portal_icon)
                image.paste(portal_icon, portal_paste_coord, portal_icon)

        # Draw zone labels
        drawn_zones.sort(key=lambda z: (self.category_settings[z[0]['category']]['label_order'], z[0]['id']))
        for zone, zone_image_rect, settings in drawn_zones:
            # Choose the fonts to draw the labels with
            label_size_multiplier = scale_factor * (zone['label_size'] if 'label_size' in zone else 0.9 if settings['special'] else 1)
            main_label_font = get_font(get_main_label_font_size(map_coord, label_size_multiplier), True)
            sub_label_font = get_font(get_sub_label_font_size(map_coord, label_size_multiplier), False)
            label_margin = get_main_label_font_size(map_coord, label_size_multiplier) // 8
            outline_width = get_text_outline_width(map_coord, label_size_multiplier)

            # Choose the location and alignment where we want to display the zone's label (center of the zone boundary unless overridden
            if 'label_rect' in zone:
                label_image_rect = map_coord.continent_to_sector_image_rect(zone['label_rect'])
            else:
                label_image_rect = zone_image_rect
            if 'label_anchor' in zone:
                label_anchor = zone['label_anchor']
                if len(label_anchor) != 2 or label_anchor[0] not in 'lmr' or label_anchor[1] not in 'tmb':
                    raise ValueError(f"Invalid label anchor: {label_anchor}")
            else:
                label_anchor = 'mm'

            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, zone_name_label_bbox[2] + 10, round(2 * label_image_rect[1][0] + 20)),
                                max(250, 10 * zone_name_label_bbox[3] + 10, round(2 * label_image_rect[1][1] + 20)))
            label_image = Image.new('RGBA', label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, 'RGBA')
            label_draw_text_anchor = label_anchor[0] + 'a'
            label_color = self.special_line_color if settings['special'] else 'white'

            # Find the ideal line wrapping for the zone's name and shape
            wrapped_zone_name_lines = wrap_zone_name(label_image_rect, label_image_size, label_margin, main_label_font, main_label_font.getmetrics(), zone, map_coord, scale_factor)

            # Draw label for the zone name
            label_pos_x = label_image.size[0] / 2 if label_anchor[0] == 'm' else 2 if label_anchor[0] == 'l' else label_image.size[0] - 2
            label_pos_y = 0
            lines_to_draw = []
            for line in wrapped_zone_name_lines:
                lines_to_draw.append((line, label_pos_y))
                label_pos_y = label_pos_y + main_label_font.getmetrics()[0] + label_margin
            for line in reversed(lines_to_draw):
                label_draw.text((label_pos_x, line[1]), line[0],
                                font=main_label_font, anchor=label_draw_text_anchor, align='center', stroke_width=outline_width, fill=label_color, stroke_fill='black')
            label_pos_y = label_pos_y + main_label_font.getmetrics()[1]

            # Draw the zone's description label (City, Dungeon etc.)
            if settings['label']:
                label_draw.text((label_pos_x, label_pos_y), settings['label'],
                                fill=label_color, font=sub_label_font, anchor=label_draw_text_anchor, stroke_width=outline_width, stroke_fill='black')
                label_pos_y = label_pos_y + sum(sub_label_font.getmetrics()) + label_margin

            # Draw the zone's level distribution label
            if settings['show_level']:
                level_text = str(zone['min_level']) if zone['min_level'] == zone['max_level'] else f"{zone['min_level']}–{zone['max_level']}"
                label_draw.text((label_pos_x, label_pos_y), level_text,
                                fill=label_color, font=sub_label_font, anchor=label_draw_text_anchor, stroke_width=outline_width, stroke_fill='black')

            # Paste the resulting label into the actual map image
            label_paste_pos = calculate_zone_label_paste_position(label_anchor, label_image, label_image_rect)
            image.paste(label_image, label_paste_pos, label_image)

    def draw_legend(self, image: Image, map_layout: MapLayout, map_coord: MapCoordinateSystem, scale_factor: float):
        font = get_font(get_legend_font_size(map_coord, scale_factor), False)
        icon_size = get_icon_size(map_coord, scale_factor)

        legend_image = Image.new('RGBA', (100 * sum(font.getmetrics()), 20 * sum(font.getmetrics())))
        legend_draw = ImageDraw.Draw(legend_image)
        legend_label_x = legend_label_y = max(8, round(2 * get_zoom_size_multiplier(map_coord, scale_factor)))
        legend_padding = 5 + math.ceil(get_line_width(map_coord, scale_factor) / 2)
        assert legend_label_x > legend_padding < legend_label_y
        for portal_type in self.portal_settings.keys():
            icon = self.get_portal_icon(portal_type, icon_size)
            legend_image.paste(icon, (legend_label_x, legend_label_y), icon)
            legend_draw_coord = legend_label_x + icon_size + 6, legend_label_y + round(icon_size / 2)
            legend_draw_text = self.portal_settings[portal_type]['legend']
            outline_width = get_text_outline_width(map_coord, scale_factor)
            legend_text_bbox = legend_draw.textbbox(legend_draw_coord, legend_draw_text, font=font, stroke_width=outline_width, anchor='lm')
            legend_draw.text(legend_draw_coord, legend_draw_text, font=font, fill='white', stroke_width=outline_width, stroke_fill='black',
                             anchor='lm')
            legend_label_y = legend_label_y + round(max(icon_size, legend_text_bbox[3] - legend_text_bbox[1]) + map_coord.zoom)
        legend_bbox = legend_image.getbbox()
        legend_image = legend_image.crop((legend_bbox[0] - legend_padding, legend_bbox[1] - legend_padding, legend_bbox[2] + legend_padding, legend_bbox[3] + legend_padding))

        legend_coord = calculate_legend_paste_position(image, legend_image.size, map_layout)
        legend_draw = ImageDraw.Draw(image, 'RGBA')
        legend_draw.rectangle(legend_coord, fill=(0, 0, 0, 160), width=get_line_width(map_coord, scale_factor), outline=(255, 255, 255, 160))
        image.paste(legend_image, legend_coord, legend_image)

    def get_portal_icon(self, portal_type, icon_size):
        if '/' not in portal_type:
            template_icon = self.portal_settings[portal_type]['icon']
            return template_icon.resize((icon_size, icon_size), resample=Image.LANCZOS)
        else:
            # Blend multiple icons together so that they're all at least partially visible despite overlapping
            blended_icon = Image.new('RGBA', (icon_size, icon_size), color=(255, 255, 255, 0))
            portal_types = portal_type.split('/')
            arc_angle = 360 / len(portal_types)
            for i, t in enumerate(portal_types):
                template_icon = self.portal_settings[t]['icon']
                resized_icon = template_icon.resize((icon_size, icon_size), resample=Image.LANCZOS)
                start_angle = i * arc_angle - 90
                end_angle = (i + 1) * arc_angle - 90
                mask = Image.new('L', (icon_size, icon_size), color='white')
                ImageDraw.Draw(mask).pieslice(((0, 0), (icon_size, icon_size)), start_angle, end_angle, width=0, fill='black')
                blended_icon = Image.composite(blended_icon, resized_icon, mask)
            return blended_icon

    def draw_portal_connection_line(self, map_image, portal1_image_coord, portal2_image_coord, portal_type, map_coord, scale_factor):
        """Draws the line between two connected far-away portals, with super-sampling for simple, if inefficient, antialiasing."""
        margin = math.ceil(max(1, get_zoom_size_multiplier(map_coord, scale_factor)))
        super_sampling_factor = 4
        line_rect = abs(portal1_image_coord[0] - portal2_image_coord[0]), abs(portal1_image_coord[1] - portal2_image_coord[1])
        paste_coord = min(portal1_image_coord[0], portal2_image_coord[0]) - margin, min(portal1_image_coord[1], portal2_image_coord[1]) - margin
        super_sampled_image_size = super_sampling_factor * (line_rect[0] + 2 * margin), super_sampling_factor * (line_rect[1] + 2 * margin)
        super_sampled_image = Image.new('RGBA', super_sampled_image_size)
        super_sampled_draw = ImageDraw.Draw(super_sampled_image)

        line_color = self.portal_settings[portal_type]['line_color']
        line_coord = ((super_sampling_factor * (portal1_image_coord[0] - paste_coord[0]), super_sampling_factor * (portal1_image_coord[1] - paste_coord[1])),
                      (super_sampling_factor * (portal2_image_coord[0] - paste_coord[0]), super_sampling_factor * (portal2_image_coord[1] - paste_coord[1])))
        super_sampled_draw.line(line_coord, fill=line_color, width=super_sampling_factor * get_line_width(map_coord, scale_factor))

        resized_size = line_rect[0] + 2 * margin, line_rect[1] + 2 * margin
        smooth_line_image = super_sampled_image.resize(resized_size, resample=Image.LANCZOS)
        map_image.paste(smooth_line_image, paste_coord, smooth_line_image)


class MasteryRegionMapOverlay(MapOverlay):
    mastery_settings = {
        'Central Tyria': {'color': (240, 51, 7)},
        'Heart of Thorns': {'color': (0, 255, 92)},
        'Path of Fire': {'color': (202, 5, 237)},
        'Icebrood Saga': {'color': (20, 153, 255)},
        'End of Dragons': {'color': (10, 240, 221)},
    }

    category_settings = {
        'city': {'order': 0, 'label_size': 1},
        'lobby': {'order': 0, 'label_size': 1},
        'open_world': {'order': 0, 'label_size': 1},
        'festival': {'order': 1, 'label_size': 0.9},
        'guild_hall': {'order': 1, 'label_size': 0.9},
        'dungeon': {'order': 3, 'label_size': 0.9},
        'raid': {'order': 3, 'label_size': 0.9},
        'strike': {'order': 3, 'label_size': 0.75},
        'story': {'order': 0, 'label_size': 0.9},
        'hybrid_instance': {'order': 2, 'label_size': 0.9},
        'lounge': {'order': 0, 'label_size': 0.75},
        'misc': {'order': 1, 'label_size': 0.75},
    }

    def draw_overlay(self, image: Image, zone_data: list[dict], map_coord: MapCoordinateSystem, scale_factor: float):
        draw = ImageDraw.Draw(image, 'RGBA')

        # Draw zone boundaries
        zone_data.sort(key=lambda z: (self.category_settings[z['category']]['order'], z['id']))
        drawn_zones = []  # list[tuple[zone, zone_image_bounds, zone_settings]]
        for zone in zone_data:
            continent_rect = zone['continent_rect']

            if not map_coord.is_rect_contained_in_sector(continent_rect):
                continue

            zone_image_rect = map_coord.continent_to_sector_image_rect(continent_rect)
            line_width = get_line_width(map_coord, scale_factor)
            outline_rect = ((zone_image_rect[0][0] - math.floor((line_width - 1) / 2), zone_image_rect[0][1] - math.floor((line_width - 1) / 2)),
                            (zone_image_rect[1][0] + math.floor(line_width / 2), zone_image_rect[1][1] + math.floor(line_width / 2)))

            mastery_color = self.mastery_settings[zone['mastery_region']]['color']
            mastery_color = mastery_color[0], mastery_color[1], mastery_color[2], 160
            draw.rectangle(outline_rect, outline='white', width=get_line_width(map_coord, scale_factor), fill=mastery_color)
            settings = self.category_settings[zone['category']]

            drawn_zones.append((zone, zone_image_rect, settings))

        for zone, zone_image_rect, settings in drawn_zones:
            # Choose the fonts to draw the labels with
            label_size_multiplier = scale_factor * (zone['label_size'] if 'label_size' in zone else settings['label_size'])
            main_label_font = get_font(get_main_label_font_size(map_coord, label_size_multiplier), True)
            sub_label_font = get_font(get_sub_label_font_size(map_coord, label_size_multiplier), False)
            label_margin = get_main_label_font_size(map_coord, label_size_multiplier) // 8
            outline_width = get_text_outline_width(map_coord, label_size_multiplier)

            # Choose the location and alignment where we want to display the zone's label (center of the zone boundary unless overridden
            if 'label_rect' in zone:
                label_image_rect = map_coord.continent_to_sector_image_rect(zone['label_rect'])
            else:
                label_image_rect = zone_image_rect
            if 'label_anchor' in zone:
                label_anchor = zone['label_anchor']
                if len(label_anchor) != 2 or label_anchor[0] not in 'lmr' or label_anchor[1] not in 'tmb':
                    raise ValueError(f"Invalid label anchor: {label_anchor}")
            else:
                label_anchor = 'mm'

            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, zone_name_label_bbox[2] + 10, round(2 * label_image_rect[1][0] + 20)),
                                max(250, 10 * zone_name_label_bbox[3] + 10, round(2 * label_image_rect[1][1] + 20)))
            label_image = Image.new('RGBA', label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, 'RGBA')
            label_draw_text_anchor = label_anchor[0] + 'a'

            # Find the ideal line wrapping for the zone's name and shape
            wrapped_zone_name_lines = wrap_zone_name(label_image_rect, label_image_size, label_margin, main_label_font, main_label_font.getmetrics(), zone, map_coord, scale_factor)

            # Draw label for the zone name
            label_pos_x = label_image.size[0] / 2 if label_anchor[0] == 'm' else 2 if label_anchor[0] == 'l' else label_image.size[0] - 2
            label_pos_y = 0
            lines_to_draw = []
            for line in wrapped_zone_name_lines:
                lines_to_draw.append((line, label_pos_y))
                label_pos_y = label_pos_y + main_label_font.getmetrics()[0] + label_margin
            for line in reversed(lines_to_draw):
                label_draw.text((label_pos_x, line[1]), line[0],
                                font=main_label_font, anchor=label_draw_text_anchor, align='center', stroke_width=outline_width, fill='white', stroke_fill='black')
            label_pos_y = label_pos_y + main_label_font.getmetrics()[1]

            # Draw the mastery region
            label_draw.text((label_pos_x, label_pos_y), zone['mastery_region'],
                            fill='white', font=sub_label_font, anchor=label_draw_text_anchor, stroke_width=outline_width, stroke_fill='black')

            # Paste the resulting label into the actual map image
            label_paste_pos = calculate_zone_label_paste_position(label_anchor, label_image, label_image_rect)
            image.paste(label_image, label_paste_pos, label_image)

    def draw_legend(self, image: Image, map_layout: MapLayout, map_coord: MapCoordinateSystem, scale_factor: float):
        font = get_font(get_main_label_font_size(map_coord, 1.3 * scale_factor), True)
        outline_width = get_text_outline_width(map_coord, scale_factor)

        title_text = 'Mastery regions'
        legend_padding = 16

        draw = ImageDraw.Draw(image)
        text_bbox = draw.textbbox((0, 0), title_text, font=font, stroke_width=outline_width, anchor='la')
        legend_size = (text_bbox[2] - text_bbox[0] + 2 * legend_padding, text_bbox[3] - text_bbox[1] + 2 * legend_padding)
        legend_coord = calculate_legend_paste_position(image, legend_size, map_layout)
        draw.text((legend_coord[0] + legend_padding, legend_coord[1] + legend_padding), title_text, font=font, fill='white', stroke_width=outline_width, stroke_fill='black',
                  anchor='la')


map_overlay_types = {
    'zone': ZoneMapOverlay,
    'mastery': MasteryRegionMapOverlay,
    'none': NoMapOverlay
}
