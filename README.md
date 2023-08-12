This is a tool for generation of map images for _Guild Wars 2_, primarily intended for use on [the game's official wiki](https://wiki.guildwars2.com/).

# Usage

By default, create a directory _tiles_ in the script's directory, unzip [that_shaman's API tiles](https://thatshaman.com/files/maps/) into it, and then
run [gw2_zone_map.py](gw2_zone_map.py) with Python. Make sure the [requirements.txt](requirements.txt) are installed.

## Parameters

| Parameter      | Default      | Description                                                                                                                                             |
|----------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| -c --continent | None         | ID of the continent to generate the map for. Mutually exclusive with -l.                                                                                |
| -l --layout    | TyriaWorld   | Name of the layout to generate the map for. Mutually exclusive with -c. Allowed values are: Tyria, Cantha, TyriaWorld                                   |
| -t --tiles     | tiles        | Name of the directory that contains the map tiles.                                                                                                      |
| -o --output    | output       | Name of the directory to generate the output maps in.                                                                                                   |
| -f --format    | jpg          | File format of the output maps.                                                                                                                         |
| -v --overlay   | zone mastery | Map overlay types to generate. Allowed values are: zone, mastery, none                                                                                  |
| -s --scale     | 1            | Scaling factor for overlays.                                                                                                                            |
| -z --zoom      | 3.3          | The zoom levels to generate the maps for. If given a decimal number, the next integer is used for map data and the map is then scaled down accordingly. |
| --lang         | en           | Experimental. The language to generate the map for: en, es, de, fr. Not fully supported yet.                                                            |
| --no-overrides |              | Turns off custom data overrides and generates the map entirely based on the official map API data.                                                      |
| --no-legend    |              | Turns off generation of map overlay legends.                                                                                                            |
