This is a tool for generation of map images for _Guild Wars 2_, primarily intended for use on [the game's official wiki](https://wiki.guildwars2.com/), such as [these](https://wiki.guildwars2.com/wiki/File:Zones.jpg) [two](https://wiki.guildwars2.com/wiki/File:Mastery_region_map.jpg) maps.

# Usage

By default, create a directory _tiles_ in the script's directory, unzip [that_shaman's API tiles](https://thatshaman.com/files/maps/) into it, and then
run [gw2_zone_map.py](gw2_zone_map.py) with Python. Make sure the [requirements.txt](requirements.txt) are installed.

## Parameters

| Parameter      | Default             | Description                                                                                                                                                                                               |
|----------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -c --continent | None                | ID of the continent to generate the map for. Mutually exclusive with -l.                                                                                                                                  |
| -l --layout    | TyriaWorld          | Name of the layout to generate the map for. Mutually exclusive with -c. Allowed values are: Tyria, Cantha, Castora, TyriaWorld                                                                            |
| -f --format    | jpg                 | File format of the output maps.                                                                                                                                                                           |
| -o --output    | output              | Name of the directory to generate the output maps in.                                                                                                                                                     |
| -s --scale     | 1                   | Scaling factor for overlays.                                                                                                                                                                              |
| -t --tiles     | local               | Source of map tile images. Allowed values are: 'local' (provided in a local directory structure, such as from that_shaman's map API), and 'api' (provided by the official tile API). Default is 'local'.  |
| -v --overlay   | zone_access mastery | Map overlay types to generate. Allowed values are: zone, zone_access, mastery, none                                                                                                                       |
| -z --zoom      | 3.4                 | The zoom levels to generate the maps for. If given a decimal number, the next integer is used for map data and the map is then scaled down accordingly.                                                   |
| --api-load     | false               | Instead of the REST API, optionally loads the API data from a local cache located in the api-cache directory, previously saved by the --api-save parameter. Can be used when the API service is down.     |
| --api-save     | false               | Optionally saves the data downloaded from the REST API to the api-cache directory, to be loaded later by the --api-load parameter in case the API service is down.                                        |
| --debug        | false               | Renders additional debugging overlays, e.g. regions for placing zone labels.                                                                                                                              |
| --lang         | en                  | Experimental. The language to generate the map for: en, es, de, fr. Not fully supported yet.                                                                                                              |
| --no-overrides |                     | Turns off custom data overrides and generates the map entirely based on the official map API data.                                                                                                        |
| --no-legend    |                     | Turns off generation of map overlay legends.                                                                                                                                                              |
| --tiles-dir    | tiles               | If tiles are set to 'local', name of the input tiles directory, such as from that_shaman's map API.                                                                                                       |
