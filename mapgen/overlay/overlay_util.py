from abc import ABC, abstractmethod
from functools import cache

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont

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
def get_main_label_font_size(map_coord: MapCoordinateSystem, size_multiplier: float = 1):
    return min(64, max(8, round(2.5 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_sub_label_font_size(map_coord: MapCoordinateSystem, size_multiplier: float = 1):
    return min(32, max(8, round(2 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_legend_font_size(map_coord: MapCoordinateSystem, size_multiplier: float = 1):
    return min(28, max(10, round(2 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_icon_size(map_coord: MapCoordinateSystem, size_multiplier: float = 1):
    return min(32, max(12, round(3 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_line_width(map_coord: MapCoordinateSystem, size_multiplier: float = 1):
    return min(32, max(1, round(0.3 * get_zoom_size_multiplier(map_coord, size_multiplier))))


@cache
def get_text_outline_width(font_size: float):
    return min(8, max(1, round(0.1 * font_size)))


def get_wrapped_text_lines(text: str, font: FreeTypeFont, line_length: int):
    lines = ['']
    for i, word in enumerate(text.split(' ')):
        line = f'{lines[-1]} {word}' if i > 0 else word
        if font.getlength(line) <= line_length or len(lines[-1]) < 3:
            lines[-1] = line
        else:
            lines.append(word)
    return lines


def wrap_label(label, font, label_margin, label_image_rect, label_image_size, map_coord, scale_factor, width_tolerance_factor=1.0):
    if label is None:
        return []

    font_metrics = font.getmetrics()
    label_box_image_width = label_image_rect[1][0] - label_image_rect[0][0]
    label_box_image_height = label_image_rect[1][1] - label_image_rect[0][1]
    height_for_max_width = 2.75 * (sum(font_metrics) + label_margin)
    height_for_min_width = 1 * (font_metrics[0] + label_margin) + height_for_max_width
    height_diff_ratio = (label_box_image_height - height_for_max_width) / (height_for_min_width - height_for_max_width)
    main_label_ideal_width = (2 - max(0, min(1, height_diff_ratio))) * label_box_image_width - get_zoom_size_multiplier(map_coord, 2 * scale_factor)
    main_label_min_width = max(4 * font_metrics[0], width_tolerance_factor * (label_box_image_width - get_zoom_size_multiplier(map_coord, 2 * scale_factor)))
    main_label_bounded_ideal_width = min(label_image_size[0], max(main_label_min_width, main_label_ideal_width))

    wrapped_zone_name_lines = []
    for input_line in label.splitlines():
        wrapped_zone_name_lines.extend(get_wrapped_text_lines(input_line, font, main_label_bounded_ideal_width))

    return wrapped_zone_name_lines


def draw_title(title_text, image, map_coord, map_layout, scale_factor):
    font_size = 2 * get_main_label_font_size(map_coord, scale_factor)
    font = get_font(font_size, True)
    outline_width = get_text_outline_width(font_size)
    legend_padding = 16
    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), title_text, font=font, stroke_width=outline_width, anchor='la')
    legend_size = (text_bbox[2] - text_bbox[0] + 2 * legend_padding, text_bbox[3] - text_bbox[1] + 2 * legend_padding)
    legend_coord = calculate_legend_paste_position(image, legend_size, map_layout)
    draw.text((legend_coord[0] + legend_padding, legend_coord[1] + legend_padding), title_text, font=font, fill='white', stroke_width=outline_width, stroke_fill='black',
              anchor='la')


def calculate_zone_label_paste_position(label_anchor, label_image: Image, label_image_rect: tuple[tuple[float, float], tuple[float, float]]):
    label_bbox = label_image.getbbox()
    label_paste_pos = [0, 0]
    match label_anchor[0]:
        case 'l':
            label_paste_pos[0] = label_image_rect[0][0]
        case 'm':
            label_paste_pos[0] = round((label_image_rect[0][0] + label_image_rect[1][0] - label_image.size[0] + 1) / 2)
        case 'r':
            label_paste_pos[0] = label_image_rect[1][0] - label_image.size[0]
    match label_anchor[1]:
        case 't':
            label_paste_pos[1] = label_image_rect[0][1]
        case 'm':
            label_paste_pos[1] = round((label_image_rect[0][1] + label_image_rect[1][1] - label_bbox[3] + label_bbox[1]) / 2) - 2
        case 'b':
            label_paste_pos[1] = label_image_rect[1][1] - label_bbox[3] + label_bbox[1] - 4
    return label_paste_pos


def calculate_legend_paste_position(image: Image, legend_size: tuple[int, int], map_layout: MapLayout):
    coord = [0, 0]
    match map_layout.legend_align[0]:
        case 'l':
            coord[0] = map_layout.legend_image_coord[0]
        case 'r':
            coord[0] = image.size[0] - map_layout.legend_image_coord[0] - legend_size[0]
    match map_layout.legend_align[1]:
        case 't':
            coord[1] = map_layout.legend_image_coord[1]
        case 'b':
            coord[1] = image.size[1] - map_layout.legend_image_coord[1] - legend_size[1]
    return coord[0], coord[1], coord[0] + legend_size[0], coord[1] + legend_size[1]


def get_zone_pos(map_coord, zone, zone_image_rect):
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
    return label_anchor, label_image_rect


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
