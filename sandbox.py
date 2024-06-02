from PIL import Image

from mapgen.overlay import ZoneMapOverlay

overlay = ZoneMapOverlay(True)
icons: list[Image] = []

for req in ['gw2', 'hot', 'lw3', 'pof', 'lw4', 'lw5', 'eod', 'soto']:
    icons.append(overlay.get_access_icon(req, 24, 2))

x_margin = 2
width = sum(icon.width + x_margin for icon in icons) - x_margin
height = max(icon.height for icon in icons)

image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
x = 0
for icon in icons:
    image.paste(icon, (x, 0), icon)
    x = x + icon.width + x_margin

image.show()
