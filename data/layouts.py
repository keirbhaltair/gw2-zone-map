from mapgen.map_coordinates import MapSector, MapLayout

_composite_sectors: dict[str, MapSector] = {
    'Tyria': MapSector(1, ((4096, 8192), (70528, 79134))),
    'Cantha': MapSector(1, ((15616, 92896), (44032, 108031))),
}

map_layouts: dict[str, MapLayout] = {
    'Tyria': MapLayout.single_sector(MapSector(1, ((18774, 8569), (70528, 68223))), legend_align='rt',
        zone_blacklist=[
         1520,  # Temple of Febe
         1523,  # Convergence: Outer Nayos
         1526,  # Inner Nayos
        ],
        portal_blacklist=[
         ("neighbor", "Inner Nayos - The Wizard's Tower")
        ],
        zone_legend_fields=['neighbor','asura_gate','dungeon','fractal','strike','raid']
     ),

    'Cantha': MapLayout.single_sector(MapSector(1, ((16128, 92896), (44544, 109055))),
        legend_align='rt',
        zone_legend_fields = ['neighbor', 'asura_gate', 'strike']
    ),

    'Castora': MapLayout.single_sector(MapSector(1, ((0, 31782), (14835, 70384))),
        legend_align='rt'
    ),

    'TyriaWorld': MapLayout([
            ((0, 0), _composite_sectors['Tyria']),
            ((16896 - _composite_sectors['Tyria'].continent_rect[0][0], _composite_sectors['Tyria'].height() - _composite_sectors['Cantha'].height()), _composite_sectors['Cantha']),
        ],
        legend_align='rt',
        zone_legend_fields=['neighbor','asura_gate','dungeon','fractal','strike','raid']
    )
}
