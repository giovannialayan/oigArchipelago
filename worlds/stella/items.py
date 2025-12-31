from BaseClasses import Item

from typing import NamedTuple, Dict

offset = 84275608_000

class StellaItem(Item):
    game = "Stella"

class ItemData(NamedTuple):
    code: int

item_table: Dict[str, ItemData] = {
    #your decks
    "first stella": ItemData(offset + 1),
    "gold stella": ItemData(offset + 2),
    "element stella": ItemData(offset + 3),
    "despair stella": ItemData(offset + 4),
    "collector stella": ItemData(offset + 5),
    "chaos stella": ItemData(offset + 6),
    "oracle stella": ItemData(offset + 7),

    #their decks
    "galaxy": ItemData(offset + 20),
    "halo": ItemData(offset + 21),
    "supercluster": ItemData(offset + 22),
    "stellar stream": ItemData(offset + 23),
    "starburst": ItemData(offset + 24),
    "blazar": ItemData(offset + 25),
    "brightest cluster": ItemData(offset + 26),

    #star cards
    "protostar": ItemData(offset + 40),
    "young star": ItemData(offset + 41),
    "subdwarf": ItemData(offset + 42),
    "subgiant": ItemData(offset + 43),
    "red giant": ItemData(offset + 44),
    "blue giant": ItemData(offset + 45),
    "bright giant": ItemData(offset + 46),
    "red supergiant": ItemData(offset + 47),
    "blue supergiant": ItemData(offset + 48),
    "hypergiant": ItemData(offset + 49),
    "ultra-cool": ItemData(offset + 50),
    "quasi-star": ItemData(offset + 51),
    "hybrid": ItemData(offset + 52),
    "exotic star": ItemData(offset + 53),
    "iron star": ItemData(offset + 54),
    "neutron": ItemData(offset + 55),
    "magnetar": ItemData(offset + 56),
    "blitzar": ItemData(offset + 57),
    "pulsar": ItemData(offset + 58),
    "boson star": ItemData(offset + 59),

    #planet cards
    "mercury": ItemData(offset + 90),
    "earth": ItemData(offset + 91),
    "mars": ItemData(offset + 92),
    "venus": ItemData(offset + 93),
    "jupiter": ItemData(offset + 94),
    "saturn": ItemData(offset + 95),
    "uranus": ItemData(offset + 96),
    "neptune": ItemData(offset + 97),
    "pluto": ItemData(offset + 98),
    "eris": ItemData(offset + 99),
    "ceres": ItemData(offset + 100),
    "makemake": ItemData(offset + 101),
    "varuna": ItemData(offset + 102),
    "apollo": ItemData(offset + 103),
    "sedna": ItemData(offset + 104),
    "varda": ItemData(offset + 105),
    "orcus": ItemData(offset + 106),
    "salacia": ItemData(offset + 107),

    #moon cards
    "ganymede": ItemData(offset + 140),
    "europa": ItemData(offset + 141),
    "moon": ItemData(offset + 142),
    "deimos": ItemData(offset + 143),
    "phobos": ItemData(offset + 144),
    "io": ItemData(offset + 145),
    "callisto": ItemData(offset + 146),
    "titan": ItemData(offset + 147),
    "rhea": ItemData(offset + 148),
    "iapetus": ItemData(offset + 149),
    "dione": ItemData(offset + 150),
    "tethys": ItemData(offset + 151),
    "enceladus": ItemData(offset + 152),
    "mimas": ItemData(offset + 153),
    "nix": ItemData(offset + 154),
    "umbriel": ItemData(offset + 155),

    #elements
    "piantus": ItemData(offset + 190),
    "acquas": ItemData(offset + 191),
    "terra": ItemData(offset + 192),
    "ventus": ItemData(offset + 193),
    "sangua": ItemData(offset + 194),
    "fulminus": ItemData(offset + 195),
    "gelos": ItemData(offset + 196),
    "suono": ItemData(offset + 197),
    "vitias": ItemData(offset + 198),
    "metallus": ItemData(offset + 199),
    "incendius": ItemData(offset + 200),
    "famea": ItemData(offset + 201),
    "vuotas": ItemData(offset + 202),
    "tenebres": ItemData(offset + 203),
    "luminoso": ItemData(offset + 204),
    "tempo": ItemData(offset + 205),
    "colores": ItemData(offset + 206),
    "stagiones": ItemData(offset + 207),
    "aviditia": ItemData(offset + 208),
    "oros": ItemData(offset + 209),
    "cristallus": ItemData(offset + 210),
    "carburantes": ItemData(offset + 211),
    "crescitia": ItemData(offset + 212),
    "evoluzio": ItemData(offset + 213),
    "mentes": ItemData(offset + 214),
    "caos": ItemData(offset + 215),
    "ordinus": ItemData(offset + 216),
    "alber": ItemData(offset + 217),
    "minerales": ItemData(offset + 218),
    "pioverus": ItemData(offset + 219),
    "movimentos": ItemData(offset + 220),
    "eternitia": ItemData(offset + 221),
    "spazios": ItemData(offset + 222),
    "visiones": ItemData(offset + 223),
    "fermoso": ItemData(offset + 224),
    "nuvolos": ItemData(offset + 225),
    "giornatas": ItemData(offset + 226),
    "nottes": ItemData(offset + 227),
    "bestias": ItemData(offset + 228),
    "direzio": ItemData(offset + 229),
    "gravitas": ItemData(offset + 230),
    "neves": ItemData(offset + 231),

    #traps
    "anomaly card": ItemData(offset + 300),
    "anomaly element": ItemData(offset + 301),
}

item_id_to_name: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}

deck_id_to_name: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and isDeck(item_name)
}

deck_name_to_id: Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code and isDeck(item_name)
}

cards: Dict[int, str] = {
    data.code: data.code for item_name, data in item_table.items() if data.code and isCard(item_name)
}

elements: Dict[int, str] = {
    data.code: data.code for item_name, data in item_table.items() if data.code and isElement(item_name)
}

traps: Dict[int, str] = {
    data.code: data.code for item_name, data in item_table.items() if data.code and isTrap(item_name)
}

def isDeck(item_name: str) -> bool: 
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 1 and item_id <= 39)

def isYourDeck(item_name: str) -> bool: 
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 1 and item_id <= 19)

def isTheirDeck(item_name: str) -> bool: 
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 20 and item_id <= 39)

def isCard(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 40 and item_id <= 189)

def isElement(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 190 and item_id <= 299)

def isTrap(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 300 and item_id <= 310)

def isProgression(item_name: str) -> bool:
    return (
        isDeck(item_name) or
        isCard(item_name) or
        isElement(item_name)
    )

def get_category(item_name: str) -> str:
    if isCard(item_name):
        return "Card"
    if isElement(item_name):
        return "Element"
    if isYourDeck(item_name):
        return "Your Deck"
    if isTheirDeck(item_name):
        return "Their Deck"
    return "Other"
