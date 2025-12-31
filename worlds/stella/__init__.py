from typing import Dict
from worlds.AutoWorld import World
from .items import StellaItem, ItemData, cards, item_table, isYourDeck, isTheirDeck, isProgression, isUseful
from .locations import StellaLocation
from .options import StellaOptions
from BaseClasses import ItemClassification

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

class StellaWorld(World):
    """
    Stella is a deck builder roguelike
    """
    game = "Stella"

    options: StellaOptions
    options_dataclass = StellaOptions

    topology_present = False

    required_difficulty = 0

    itempool: list

    def generate_early(self):
        self.required_difficulty = self.options.difficulty_to_win
        
    def create_items(self):
        your_decks_to_unlock = self.options.your_decks_unlocked_from_start
        their_decks_to_unlock = self.options.their_decks_unlocked_from_start

        excluded_items = Dict[str, ItemData] = {}

        your_deck_table: Dict[str, ItemData] = {}
        their_deck_table: Dict[str, ItemData] = {}
        for item in item_table:
            if (isYourDeck(item)):
                your_deck_table[item] = item_table[item]
            elif (isTheirDeck(item)):
                their_deck_table[item] = item_table[item]

        your_deck_tuple_list = list(your_deck_table.items())
        their_deck_tuple_list = list(their_deck_table.items())
        for i in range(your_decks_to_unlock):
            deck = self.random.choice(your_deck_tuple_list)
            deck_name = deck[0]
            deck_data = deck[1]

            precollected_item = self.create_item(deck_name, ItemClassification.progression)
            self.multiworld.push_precollected(precollected_item)
            excluded_items[deck_name] = deck_data
            your_deck_tuple_list.remove(deck)

        for i in range(their_decks_to_unlock):
            deck = self.random.choice(their_deck_tuple_list)
            deck_name = deck[0]
            deck_data = deck[1]

            precollected_item = self.create_item(deck_name, ItemClassification.progression)
            self.multiworld.push_precollected(precollected_item)
            excluded_items[deck_name] = deck_data
            their_deck_tuple_list.remove(deck)

        self.itempool = []
        for item_name in item_table:

            classification = ItemClassification.filler
            if isProgression(item_name):
                classification = ItemClassification.progression
            
            self.itempool.append(self.create_item(item_name, classification))

        self.multiworld.itempool += self.itempool
