from BaseClasses import Location
from .items import deck_id_to_name, elements, cards

max_shop_card_checks = 100
max_shop_element_checks = 100

offset = 84275609_000

class StellaLocation(Location):
    game = "Stella"
    lightyear: str = None
    deck: str = None
    difficulty: str = None

stella_location_name_to_id = dict()
stella_location_id_to_name = dict()
stella_location_id_to_difficulty = dict()
stella_location_id_to_lightyear = dict()

prev_id = offset

for deck in deck_id_to_name:
    for lightyear in range(10):
        for difficulty in range(11):
            location_name = deck_id_to_name[deck] + " lightyear " + \
                str(lightyear + 1) + " difficulty " + str(difficulty)
            location_id = prev_id
            prev_id += 1
            stella_location_name_to_id[location_name] = location_id
            stella_location_id_to_name[location_id] = location_name
            stella_location_id_to_difficulty[location_id] = difficulty
            stella_location_id_to_lightyear[location_id] = lightyear + 1

card_id_offset = prev_id + 1

for i in range(6):
    for j in range(max_shop_card_checks):
        prev_id += 1
        location_name = "Shop card " + str(j + 1) + " at difficulty " + str(i)
        location_id = prev_id

        stella_location_name_to_id[location_name] = location_id
        stella_location_id_to_name[location_id] = location_name

element_id_offset = prev_id + 1

for i in range(6):
    for j in range(max_shop_element_checks):
        prev_id += 1
        location_name = "Shop element " + str(j + 1) + " at difficulty " + str(i)
        location_id = prev_id

        stella_location_name_to_id[location_name] = location_id
        stella_location_id_to_name[location_id] = location_name

diffiulty_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]