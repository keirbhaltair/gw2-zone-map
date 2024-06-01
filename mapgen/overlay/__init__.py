import mapgen.overlay.mastery_overlay
import mapgen.overlay.overlay_util
import mapgen.overlay.zone_overlay
from mapgen.overlay.mastery_overlay import MasteryRegionMapOverlay
from mapgen.overlay.overlay_util import NoMapOverlay
from mapgen.overlay.zone_overlay import ZoneMapOverlay

map_overlays = {
    'zone': ZoneMapOverlay(False),
    'zone_access': ZoneMapOverlay(True),
    'mastery': MasteryRegionMapOverlay(False),
    'mastery_access': MasteryRegionMapOverlay(True),
    'none': NoMapOverlay()
}
