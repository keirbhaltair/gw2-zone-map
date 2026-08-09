from typing import Any

# Overlays to be placed on top of official tile API map art source, in case it's out of date
tile_api_map_overlays: list[dict[str, Any]] = [
    # Eternity's Garden
    {
        "map_id": 1622,
        "continent_id": 1,
        "continent_rect": (
            (12 * 256, 234 * 256),
            ((21 + 1) * 256, (246 + 1) * 256)
        ),
        "image_url": "https://wiki.guildwars2.com/images/d/d3/Eternity's_Garden_map_overlay.webp"
    }
]
