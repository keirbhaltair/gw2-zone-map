from mapgen.map_coordinates import MapSector, MapLayout

# TODO add layout-specific zone blacklist

_composite_sectors: dict[str, MapSector] = {
    'Tyria': MapSector(1, ((18411, 12725), (70016, 67071))),
    'Cantha': MapSector(1, ((18176, 94944), (41471, 108031))),
}

map_layouts: dict[str, MapLayout] = {
    'Tyria': MapLayout.single_sector(MapSector(1, ((21078, 12853), (70016, 65151))), legend_align='rt'),
    'Cantha': MapLayout.single_sector(MapSector(1, ((18688, 94944), (40959, 107775))), legend_align='rt'),
    'TyriaWorld': MapLayout([
        ((0, 0), _composite_sectors['Tyria']),
        ((0, _composite_sectors['Tyria'].height() - _composite_sectors['Cantha'].height()), _composite_sectors['Cantha']),
    ], legend_align='rt')
}
