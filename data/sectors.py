from mapgen.map_coordinates import MapSector, MapComposite

sectors: dict[str, MapSector] = {
    'Tyria': MapSector(1, ((31744, 15871), (70016, 65023))),
    'Cantha': MapSector(1, ((18688, 94944), (40959, 107775))),
}

_composite_sectors: dict[str, MapSector] = {
    'Tyria': MapSector(1, ((28160, 15615), (70016, 67071))),
    'Cantha': MapSector(1, ((19712, 95200), (39935, 107519))),
}

composites_by_continent_id: dict[int, MapComposite] = {
    1: MapComposite([
        ((0, 0), _composite_sectors['Tyria']),
        ((0, _composite_sectors['Tyria'].continent_rect[1][1] - _composite_sectors['Tyria'].continent_rect[0][1]
          - _composite_sectors['Cantha'].continent_rect[1][1] + _composite_sectors['Cantha'].continent_rect[0][1]),
         _composite_sectors['Cantha']),
    ])
}
