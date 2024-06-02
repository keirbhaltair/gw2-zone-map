import math
from dataclasses import dataclass

from data.portals import portals
from mapgen.overlay.overlay_util import *


class ZoneMapOverlay(MapOverlay):
    def __init__(self, show_access_requirements: bool):
        super().__init__()
        self.show_access_requirements = show_access_requirements

    base_line_color = (255, 255, 255, 255)
    special_line_color = (255, 160, 15, 255)

    access_settings = {
        'gw2': {'label': 'Core', 'icon': get_image("https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png")},
        'lw1': {'label': 'Core', 'icon': get_image("https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png")},
        'lw2': {'label': 'Core', 'icon': get_image("https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png")},
        'hot': {'label': 'HoT', 'icon': get_image("https://wiki.guildwars2.com/images/thumb/5/52/HoT_Texture_Centered_Trans.png/240px-HoT_Texture_Centered_Trans.png")},
        'lw3': {'label': 'LW3', 'icon': get_image("https://wiki.guildwars2.com/images/thumb/c/ca/Living_World_Season_3_logo.png/320px-Living_World_Season_3_logo.png")},
        'pof': {'label': 'PoF', 'icon': get_image("https://wiki.guildwars2.com/images/a/a7/PoF_Texture_Trans.png")},
        'lw4': {'label': 'LW4', 'icon': get_image("https://wiki.guildwars2.com/images/a/a1/Living_World_Season_4_logo.png")},
        'lw5': {'label': 'IBS', 'icon': get_image("https://wiki.guildwars2.com/images/1/19/Living_World_Season_5_logo.png")},
        'eod': {'label': 'EoD', 'icon': get_image("https://wiki.guildwars2.com/images/thumb/c/cc/EoD_Texture_Trans.png/240px-EoD_Texture_Trans.png")},
        'soto': {'label': 'SotO', 'icon': get_image("https://wiki.guildwars2.com/images/4/44/Secrets_of_the_Obscure_logo.png")},
    }

    category_settings = {
        'city': {'boundary_order': 0, 'label_order': 2, 'special': False, 'show_level': False, 'label': 'City'},
        'lobby': {'boundary_order': 0, 'label_order': 2, 'special': False, 'show_level': False, 'label': 'Lobby'},
        'outpost': {'boundary_order': 0, 'label_order': 2, 'special': False, 'show_level': False, 'label': 'Outpost'},
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
        'neighbor': {
            'icon': get_image("https://wiki.guildwars2.com/images/a/ae/Asura_gate_starter_area_%28map_icon%29.png"),
            'line_color': (45, 185, 227, 150),
            'legend': 'Zone portal'
        },
        'asura_gate': {
            'icon': get_image("https://wiki.guildwars2.com/images/6/6c/Asura_gate_%28map_icon%29.png"),
            'line_color': None,
            'legend': 'Asura gate / Long distance portal'
        },
        'dungeon': {
            'icon': get_image("https://wiki.guildwars2.com/images/3/3c/Dungeon_%28map_icon%29.png"),
            'line_color': None,
            'legend': 'Dungeon'
        },
        'fractal': {
            'icon': get_image("https://wiki.guildwars2.com/images/9/9f/Fractals_of_the_Mists_%28map_icon%29.png"),
            'line_color': None,
            'legend': 'Fractals of the Mists'
        },
        'strike': {
            'icon': get_image("https://wiki.guildwars2.com/images/e/e7/Strike_Mission_%28map_icon%29.png"),
            'line_color': None,
            'legend': 'Strike mission'
        },
        'raid': {
            'icon': get_image("https://wiki.guildwars2.com/images/8/86/Raid_%28map_icon%29.png"),
            'line_color': (199, 76, 42, 150),
            'legend': 'Raid'
        },
    }

    @dataclass
    class TextLine:
        text: str
        pos_y: float
        font: FreeTypeFont
        outline_width: int
        access_req: str = None

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
            main_label_font_size = get_main_label_font_size(map_coord, label_size_multiplier)
            main_label_font = get_font(main_label_font_size, True)
            main_label_line_margin = main_label_font_size // 8
            main_label_outline_width = get_text_outline_width(main_label_font_size)
            sub_label_font_size = get_sub_label_font_size(map_coord, label_size_multiplier)
            sub_label_font = get_font(sub_label_font_size, False)
            sub_label_outline_width = get_text_outline_width(sub_label_font_size)

            # Choose the location and alignment where we want to display the zone's label (center of the zone boundary unless overridden)
            label_anchor, label_image_rect = get_zone_pos(map_coord, zone, zone_image_rect)

            # Create a temporary image to draw the labels in, so that we can easily center them in the final map regardless of line count
            zone_name_label_bbox = draw.textbbox((0, 0), zone['name'], font=main_label_font)
            label_image_size = (max(250, zone_name_label_bbox[2] + 10, round(2 * label_image_rect[1][0] + 20)),
                                max(250, 10 * zone_name_label_bbox[3] + 10, round(2 * label_image_rect[1][1] + 20)))
            label_image = Image.new('RGBA', label_image_size, (255, 255, 255, 0))
            label_draw = ImageDraw.Draw(label_image, 'RGBA')
            label_draw_text_anchor = label_anchor[0] + 'a'
            label_color = self.special_line_color if settings['special'] else 'white'

            # Collect all lines to draw so that they can be drawn in reverse order to keep earlier lines on top
            lines_to_draw: list[ZoneMapOverlay.TextLine] = []

            # Find the ideal line wrapping for the zone's name and shape
            wrapped_zone_name_lines = wrap_label(zone['name'], main_label_font, main_label_line_margin, label_image_rect, label_image_size, map_coord, scale_factor)

            # Draw label for the zone name
            label_pos_x = label_image.size[0] / 2 if label_anchor[0] == 'm' else 2 if label_anchor[0] == 'l' else label_image.size[0] - 2
            label_pos_y = 0
            for line in wrapped_zone_name_lines:
                lines_to_draw.append(self.TextLine(line, label_pos_y, main_label_font, main_label_outline_width))
                label_pos_y = label_pos_y + main_label_font.getmetrics()[0] + main_label_line_margin
            label_pos_y = label_pos_y + max(0, main_label_font.getmetrics()[1] - main_label_line_margin)

            sub_label_lines = self.get_sub_label_lines(zone, settings)
            for (line_text, icon) in sub_label_lines:
                lines_to_draw.append(self.TextLine(line_text, label_pos_y, sub_label_font, sub_label_outline_width, icon))
                label_pos_y = label_pos_y + sum(sub_label_font.getmetrics()) + main_label_line_margin

            # Perform the actual draws
            for line in reversed(lines_to_draw):
                self.draw_text_line(line, label_pos_x, label_color, label_image, label_draw, label_draw_text_anchor)

            # Paste the resulting label into the actual map image
            label_paste_pos = calculate_zone_label_paste_position(label_anchor, label_image, label_image_rect)
            image.paste(label_image, label_paste_pos, label_image)

    def get_sub_label_lines(self, zone, settings) -> list[tuple[str, Image]]:
        sub_label_text = None
        access_req = None

        if settings['label']:
            # Zone's description label (City, Dungeon etc.)
            sub_label_text = settings['label']
        elif settings['show_level']:
            # Zone's level distribution label
            sub_label_text = str(zone['min_level']) if zone['min_level'] == zone['max_level'] else f"{zone['min_level']}–{zone['max_level']}"

        if self.show_access_requirements:
            access_req = zone['access_req']
            access = self.access_settings[access_req]
            sub_label_text = f'{access['label']} · {sub_label_text}' if sub_label_text else access['label']

        return [(sub_label_text, access_req)] if sub_label_text else []

    def draw_text_line(self, line: TextLine, label_pos_x, label_color, label_image, label_draw, label_draw_text_anchor):
        pos_x_text_offset = 0
        icon_height = line.font.getmetrics()[0]
        icon = self.get_access_icon(line.access_req, icon_height, 1)
        text = f' {line.text}' if icon else line.text

        if icon:
            icon_offset_multiplier = 1 if label_draw_text_anchor[0] == 'r' else 0.5 if label_draw_text_anchor[0] == 'm' else 0
            icon_coord = (
                round(label_pos_x - icon_offset_multiplier * (line.font.getlength(text) + icon.size[0])),
                round(line.pos_y - (icon.size[1] - sum(line.font.getmetrics())) / 2)
            )
            label_image.paste(icon, icon_coord, icon)
            pos_x_text_offset = (1 - icon_offset_multiplier) * icon.size[0]

        label_draw.text((label_pos_x + pos_x_text_offset, line.pos_y), text,
                        font=line.font, anchor=label_draw_text_anchor, align='center', stroke_width=line.outline_width, fill=label_color, stroke_fill='black')

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
            outline_width = get_text_outline_width(get_legend_font_size(map_coord, scale_factor))
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

    @cache
    def get_access_icon(self, access_req: str, icon_size: int, stroke_width: int | None):
        if not access_req:
            return None
        template_icon = self.access_settings[access_req]['icon']
        if not template_icon:
            return None
        template_icon = template_icon.crop(template_icon.getbbox())

        # Resize, while increasing the channel alpha, since the logos have very thin lines, which become very transparent after downscaling
        (width, height) = (round(template_icon.width * icon_size / template_icon.height), icon_size)
        icon = template_icon.resize((width, height), resample=Image.Resampling.LANCZOS)
        icon_alpha = np.asarray(icon)[..., 3]
        icon_alpha = np.cbrt(icon_alpha.astype(float) / 255) * 255
        icon_alpha = np.clip(icon_alpha, 0, 255).astype(np.uint8)
        icon_alpha_image = Image.fromarray(icon_alpha, 'L')
        icon.putalpha(icon_alpha_image)

        if stroke_width is None:
            return icon
        else:
            return add_stroke_around_alpha(icon, stroke_width=stroke_width, alpha_threshold=64)

    @cache
    def get_portal_icon(self, portal_type: str, icon_size: int):
        if '/' not in portal_type:
            template_icon = self.portal_settings[portal_type]['icon']
            return template_icon.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS)
        else:
            # Blend multiple icons together so that they're all at least partially visible despite overlapping
            blended_icon = Image.new('RGBA', (icon_size, icon_size), color=(255, 255, 255, 0))
            portal_types = portal_type.split('/')
            arc_angle = 360 / len(portal_types)
            for i, t in enumerate(portal_types):
                template_icon = self.portal_settings[t]['icon']
                resized_icon = template_icon.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS)
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
        smooth_line_image = super_sampled_image.resize(resized_size, resample=Image.Resampling.LANCZOS)
        map_image.paste(smooth_line_image, paste_coord, smooth_line_image)