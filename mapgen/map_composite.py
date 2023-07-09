from PIL import Image, ImageDraw


def combine_part_images(parts: list[tuple[(int, int), Image]]) -> Image:
    total_size = (max(pi[0][0] + pi[1].size[0] for pi in parts),
                  max(pi[0][1] + pi[1].size[1] for pi in parts))

    full_image = Image.new('RGB', total_size)
    full_image_draw = ImageDraw.Draw(full_image, 'RGBA')
    outline_width = 7

    for part in parts:
        part_top_left = part[0]
        part_image = part[1]
        part_rect = (part_top_left[0] - outline_width,
                     part_top_left[1] - outline_width,
                     part_top_left[0] + part_image.size[0] + outline_width - 1,
                     part_top_left[1] + part_image.size[1] + outline_width - 1)
        full_image_draw.rectangle(part_rect, width=outline_width, outline=(255, 255, 255, 95))
        full_image.paste(part_image, part_top_left)

    return full_image
