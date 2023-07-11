This is a tool for generation of map images for _Guild Wars 2_, primarily intended for use on [the game's official wiki](https://wiki.guildwars2.com/).

# Usage

By default, create a directory _tiles_ in the script's directory, unzip [that_shaman's API tiles](https://thatshaman.com/files/maps/) into it, and then
run [gw2_zone_map.py](gw2_zone_map.py) with Python. Make sure the [requirements.pip](requirements.pip) are installed.

## Parameters

| Parameter      | Default    | Description                                                                                                                                                          |
|----------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -c --continent | None       | ID of the continent to generate the map for. Mutually exclusive with -l.                                                                                             |
| -l --layout    | TyriaWorld | Name of the layout to generate the map for. Mutually exclusive with -c. Allowed values are: Tyria, Cantha, TyriaWorld                                                |
| -t --tiles     | tiles      | Name of the directory that contains the map tiles.                                                                                                                   |
| -o --output    | output     | Name of the directory to generate the output maps in.                                                                                                                |
| -v --overlay   | All        | Map overlay types to generate. Allowed values are: zone, mastery, none                                                                                               |
| -z --zoom      | 3          | The zoom levels to generate the maps for. Technically any zoom level you have tiles for should be supported, but the label placement is mostly optimized for zoom 3. |
| --lang         | en         | Experimental. The language to generate the map for: en, es, de, fr. Not fully supported yet.                                                                         |
| --no-overrides |            | Turns off custom data overrides and generates the map entirely based on the official map API data.                                                                   |
| --no-legend    |            | Turns off generation of map overlay legends.                                                                                                                         |
