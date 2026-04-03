from typing import Dict, Union, List
from worlds.AutoWorld import World, WebWorld
from .items import StellaItem, ItemData, cards, item_table, isYourDeck, isTheirDeck, isProgression, isUseful, isGoal, isTrap, isFiller, item_name_to_id, item_id_to_name, deck_id_to_name, \
cards_and_elements, elements
from .items import offset as item_offset
from .locations import StellaLocation, stella_location_name_to_id, stella_location_id_to_name, stella_location_id_to_difficulty, stella_location_id_to_lightyear, \
card_id_offset, element_id_offset, max_shop_card_checks, max_shop_element_checks, diffiulty_list
from .options import StellaOptions, Goal, DecksToWin, DifficultyToWin
from BaseClasses import ItemClassification, Region, LocationProgressType, CollectionState, Tutorial
from worlds.generic.Rules import add_rule

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

class StellaWebWorld(WebWorld):
    theme = "grassFlowers"
    bug_report_page = ""
    rich_text_options_doc = True
    setup_en = Tutorial(
        "Stella guide",
        "how to play Stella with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["oig"]
    )

    tutorials = [setup_en]

class StellaWorld(World):
    """
    Stella is a deck builder roguelike
    """
    game = "Stella"
    web = StellaWebWorld()

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

    difficulties_with_checks = []

    distributed_fillers = dict()

    itempool: list

    def generate_early(self):
        self.required_difficulty = self.options.difficulty_to_win.value
        self.difficulties_with_checks = list(self.options.difficulties_with_checks.value)
        
    def create_items(self):
        your_decks_to_unlock = self.options.your_decks_unlocked_from_start.value
        their_decks_to_unlock = self.options.their_decks_unlocked_from_start.value

        excluded_items: Dict[str, ItemData] = {}

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
            if not item_name in excluded_items and not isTrap(item_name) and not isFiller(item_name) and not isGoal(item_name):
                self.itempool.append(self.create_item(item_name))

        pool_remaining = self.locations_set - len(self.itempool)
        for i in range(pool_remaining):
            trap_chance = self.random.randint(1, 100)
            if (trap_chance <= self.options.traps.value):
                trap_id = self.random.randint(300, 306)
                self.itempool.append(self.create_item(item_id_to_name[trap_id + item_offset]))
            else:
                filler_id = self.random.randint(320, 326)
                self.itempool.append(self.create_item(item_id_to_name[filler_id + item_offset]))

        self.multiworld.itempool += self.itempool

    def create_item(self, item: Union[str, ItemData]):
        item_name = ""
        if isinstance(item, str):
            item_name = item
            item = item_table[item]
        else:
            item_name = item

        classification = ItemClassification.filler

        if isProgression(item_name):
            classification = ItemClassification.progression
        elif isUseful(item_name):
            classification = ItemClassification.useful

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

                    if (str(difficulty) in self.difficulties_with_checks):
                        new_location = StellaLocation(self.player, location, location_id, deck_region)

                        new_location.deck = deck_name
                        new_location.difficulty = difficulty
                        new_location.lightyear = lightyear

                        new_location.progress_type = LocationProgressType.DEFAULT

                        # if lightyear >= 5:
                        #     add_rule(new_location, lambda state, _lightyear_=lightyear: state.has_from_list(list(cards_and_elements.values()), self.player, 2 + _lightyear_))

                        # if lightyear > 3:
                        #     add_rule(new_location, lambda state, _difficulty_=difficulty: state.has_from_list(list(elements.values()), self.player, _difficulty_ * 3))

                        if difficulty != 0:
                            add_rule(new_location, lambda state, _deck_name_=deck_name, _lightyear_=lightyear, _difficulty_=difficulty: state.can_reach_location(
                            _deck_name_ + " lightyear " + str(_lightyear_) + " difficulty " + str(_difficulty_ - 1), self.player))

                        self.locations_set += 1
                        all_locations.append(new_location)
                        deck_region.locations.append(new_location)

            # place event items for deck completion tracking
            goal_name = deck_name + " completion progression"
            goal_location = StellaLocation(self.player, goal_name, None, deck_region)
            goal_location.place_locked_item(item_table[goal_name])

            deck_region.locations.append(goal_location)

            self.multiworld.regions.append(deck_region)

            # note: might need more here for deck difficulties?
            menu_region.connect(deck_region, None, lambda state, _deck_name_=deck_name: state.has(_deck_name_, self.player))

    def set_rules(self):
        def get_goal_count(state: CollectionState):
            count = 0
            for item_name in item_table:
                if isGoal(item_name) and state.has(item_name, self.player):
                    count+=1
            return count
        
        # option_beat_decks: goal item is rewarded in game upon completing lightyear 10 for the first time on a deck
        # option_beat_decks_on_difficulty: same as above but the game will reward it only on the specified difficulty
        # option_beat_difficulty: same as above

        if self.options.goal.value == Goal.option_beat_decks or self.options.goal.value == Goal.option_beat_decks_on_difficulty:
            self.multiworld.completion_condition[self.player] = lambda state: get_goal_count(state) >=  self.options.decks_to_win.value    
        elif self.options.goal.value == Goal.option_beat_difficulty:
            self.multiworld.completion_condition[self.player] = lambda state: get_goal_count(state) >= 1    

    def fill_slot_data(self):
        min_price = self.options.minimum_shop_price.value
        max_price = self.options.maximum_shop_price.value

        if min_price > max_price:
            min_price, max_price = max_price, min_price

        base_data = {
            "goal": self.options.goal.value,
            "decks_to_win": self.options.decks_to_win.value,
            "difficulties_with_checks": self.difficulties_with_checks,
            "required_difficulty": self.options.difficulty_to_win.value,
            "min_price": min_price,
            "max_price": max_price,
            "deathlink": bool(self.options.death_link)
        }
        return base_data
        