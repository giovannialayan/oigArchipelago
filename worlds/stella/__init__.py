from typing import Dict, Union, List
from worlds.AutoWorld import World
from .items import StellaItem, ItemData, cards, item_table, isYourDeck, isTheirDeck, isProgression, item_name_to_id, item_id_to_name, deck_id_to_name, cards_and_elements
from .items import offset as item_offset
from .locations import StellaLocation, stella_location_name_to_id, stella_location_id_to_name, stella_location_id_to_difficulty, stella_location_id_to_lightyear
from .options import StellaOptions
from BaseClasses import ItemClassification, Region, LocationProgressType
from worlds.generic.Rules import add_rule

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

class StellaWorld(World):
    """
    Stella is a deck builder roguelike
    """
    game = "Stella"

    options: StellaOptions
    options_dataclass = StellaOptions

    topology_present = False

    locations_set = 0
    shop_card_locations = dict()
    shop_element_locations = dict()

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = stella_location_id_to_name
    location_name_to_id = stella_location_name_to_id

    required_difficulty = 0

    distributed_fillers = dict()

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

            precollected_item = self.create_item(deck_name)
            self.multiworld.push_precollected(precollected_item)
            excluded_items[deck_name] = deck_data
            your_deck_tuple_list.remove(deck)

        for i in range(their_decks_to_unlock):
            deck = self.random.choice(their_deck_tuple_list)
            deck_name = deck[0]
            deck_data = deck[1]

            precollected_item = self.create_item(deck_name)
            self.multiworld.push_precollected(precollected_item)
            excluded_items[deck_name] = deck_data
            their_deck_tuple_list.remove(deck)

        self.itempool = []
        for item_name in item_table:
            self.itempool.append(self.create_item(item_name))

        for i in range(self.options.traps):
            trap_id = self.random.randint(300, 306)
            self.itempool.append(self.create_item(item_id_to_name[trap_id + item_offset]))

        pool_remaining = self.locations_set - len(self.itempool)
        for i in range(pool_remaining):
            filler_id = self.random.randint(320, 326)
            self.itempool.append(self.create_item(filler_id))

        self.multiworld.itempool += self.itempool

    def create_item(self, item: Union[str, ItemData]):
        item_name = ""
        if isinstance(item, str):
            item_name = item
            item = item_table[item]
        else:
            item_name = item_table[item]

        classification = ItemClassification.filler

        if isProgression(item_name):
            classification = ItemClassification.progression

        if classification is ItemClassification.filler:
            if self.distributed_fillers.get(item_name) is None:
                self.distributed_fillers[item_name] = 1
            else:
                self.distributed_fillers[item_name] += 1

        return StellaItem(item_name, classification, item.code, self.player)
    
    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)

        self.multiworld.regions.append(menu_region)
        all_locations: List[StellaLocation] = list()

        for deck in deck_id_to_name:
            deck_name = deck_id_to_name[deck]
            deck_region = Region(deck_name, self.player, self.multiworld)
            for location in stella_location_name_to_id:
                if str(location).startswith(deck_name):
                    location_id = stella_location_name_to_id[location]
                    difficulty = stella_location_id_to_difficulty[location_id]
                    lightyear = stella_location_id_to_lightyear[location_id]
                    new_location = StellaLocation(self.player, location, location_id, deck_region)

                    new_location.deck = deck_name
                    new_location.difficulty = difficulty
                    new_location.lightyear = lightyear

                    new_location.progress_type = LocationProgressType.DEFAULT

                    if lightyear >= 5:
                        add_rule(new_location, lambda state, _lightyear_=lightyear: state.has_from_list(list(cards_and_elements.values()), self.player, 4 + _lightyear_ * 2))