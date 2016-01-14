import re

unrandomized_card_types = ["Knight","Shelter","Ruins","Prize","Event"]

unrandomized_card_names = ["Spoils","Madman","Mercenary","Colony","Platinum","Potion"]

unrandomized_card_rules = "not in the Supply"

not_stuff = "CardType NOT REGEXP '" + "|".join(unrandomized_card_types) \
            + "' AND CardName NOT REGEXP '" + "|".join(unrandomized_card_names) + \
            "' AND Rules NOT REGEXP '" + unrandomized_card_rules + "'"


def blacklist(names):
    if re.search('^$', names):
        none_of_these_cards = unrandomized_card_names
    else:
        listed_cards = re.split(', ?', names)
        none_of_these_cards = unrandomized_card_names + listed_cards
    exclusion_string = "CardType NOT REGEXP '" + "|".join(unrandomized_card_types) \
            + "' AND CardName NOT REGEXP '" + "|".join(none_of_these_cards) + \
            "' AND Rules NOT REGEXP '" + unrandomized_card_rules + "'"
    return exclusion_string


# print "|".join(unrandomized_card_types)

