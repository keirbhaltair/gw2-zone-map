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
    },

    # Leyspring Hollows
    {
        "map_id": 1633,
        "continent_id": 1,
        "continent_rect": (
            (12 * 256, 224 * 256),
            ((24 + 1) * 256, (233 + 1) * 256)
        ),
        "image_url": "https://wiki.guildwars2.com/images/c/c3/Leyspring_Hollows_map_overlay.webp"
    }
]

# Regions for the 'mixed' tile source per continent ID where local file system's tiles should be used instead of the official API.
# To be used when the official API is not up-to-date in a certain region, but updated local tile files exist (such as those from that_shaman).
tile_mixed_map_local_regions = {
    1: [  # Continent: Tyria
        [[0, 0], [81920, 8960]],  # Top of the continent
        [[0, 111104], [81920, 114688]],  # Bottom of the continent
        [[0, 32768], [16384, 72704]],  # Castora
    ]
}
