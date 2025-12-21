from worlds.AutoWorld import World
from .items import StellaItem
from .locations import StellaLocation
from .options import StellaOptions

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

class StellaWorld(World):
    """
    Stella is a deck builder roguelike
    """
    game = "Stella"

    options: StellaOptions
    options_dataclass = StellaOptions

    topology_present = False

