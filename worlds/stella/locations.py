from BaseClasses import Location
from .items import deck_id_to_name

offset = 84275609_000

diffiulty_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
        for difficulty in diffiulty_list:
            location_name = deck_id_to_name[deck] + " lightyear " + \
                str(lightyear + 1) + " difficulty " + str(difficulty)
            location_id = prev_id
            prev_id += 1
            stella_location_name_to_id[location_name] = location_id
            stella_location_id_to_name[location_id] = location_name
            stella_location_id_to_difficulty[location_id] = difficulty
            stella_location_id_to_lightyear[location_id] = lightyear + 1

goal_list = [
    "first stella completed", 
    "gold stella completed", 
    "element stella completed",
    "despair stella completed",
    "collector stella completed",
    "chaos stella completed",
    "oracle stella completed",
    "galaxy completed",
    "halo completed",
    "supercluster completed",
    "stellar stream completed",
    "starburst completed",
    "blazar completed",
    "brightest cluster completed",
]

for goal in goal_list:
    location_id = prev_id
    prev_id += 1
    stella_location_name_to_id[goal] = location_id
    stella_location_id_to_name[location_id] = goal