from mapgen.map_coordinates import MapSector, MapLayout

_composite_sectors: dict[str, MapSector] = {
    'Tyria': MapSector(1, ((28160, 15615), (70016, 67071))),
    'Cantha': MapSector(1, ((19712, 95200), (39935, 107519))),
}

map_layouts: dict[str, MapLayout] = {
    'Tyria': MapLayout.single_sector(MapSector(1, ((31744, 15871), (70016, 65023)))),
    'Cantha': MapLayout.single_sector(MapSector(1, ((18688, 94944), (40959, 107775))), legend_align='rt'),
    'TyriaWorld': MapLayout([
        ((0, 0), _composite_sectors['Tyria']),
        ((0, _composite_sectors['Tyria'].height() - _composite_sectors['Cantha'].height()), _composite_sectors['Cantha']),
    ])
}
