from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Range, Choice

class Goal(Choice):
    """
    the goal for Stella
    beat decks: win with specified number of unique decks
    beat difficulty: win on specified difficulty with any deck
    beat decks on difficulty: win with specified number of unique decks on specified difficulty
    """
    display_name = "goal"
    option_beat_decks = 0
    option_beat_difficulty = 1
    option_beat_decks_on_difficulty = 2
    default = 0

class DecksToWin(Range):
    """
    when the goal "beat decks" or "beat decks on difficulty" is selected, the number of decks required to complete the archipelago run
    """
    display_name = "required decks to win"
    range_start = 1
    range_end = 16
    default = 6

class DifficultyToWin(Range):
    """
    when the goal "beat difficulty" or "beat decks on difficulty" is selected, the difficulty required to complete the archipelago run
    """
    display_name = "required difficulty to win"
    range_start = 1
    range_end = 10
    default = 5

class MinimumShopPrice(Range):
    """the minimum price for an AP item in the shop"""
    display_name = "minimum AP item price in shop"
    range_start = 1
    range_end = 50
    default = 1


class MaximumShopPrice(Range):
    """the maximum price for an AP item in the shop"""
    display_name = "maximum AP item price in shop"
    range_start = 1
    range_end = 200
    default = 30

class YourDecksUnlockedFromStart(Range):
    """number of random stella decks you want to start with."""
    display_name = "number of starting stella decks"
    range_start = 1
    range_end = 8
    default = 1

class TheirDecksUnlockedFromStart(Range):
    """number of random cosmic decks you want to start with."""
    display_name = "number of starting cosmic decks"
    range_start = 1
    range_end = 8
    default = 1

class DeathLink(Toggle):
    """when your run ends, everybody will die. when somebody else dies, your run will end."""
    display_name = "Death Link"

class Traps(Range):
    """percentage of filler items that will be traps"""
    display_name = "trap percentage of filler items"
    range_start = 0
    range_end = 100
    default = 15

@dataclass
class StellaOptions(PerGameCommonOptions):
    goal: Goal
    decks_to_win: DecksToWin
    difficulty_to_win: DifficultyToWin
    minimum_shop_price: MinimumShopPrice
    maximum_shop_price: MaximumShopPrice
    your_decks_unlocked_from_start: YourDecksUnlockedFromStart
    their_decks_unlocked_from_start: TheirDecksUnlockedFromStart
    death_link: DeathLink
    traps: Traps