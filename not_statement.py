import re
import string

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
        listed_cards = re.split(",|;|\t|\r?\n", names)
        listed_cards = map(string.strip, listed_cards)

        none_of_these_cards = unrandomized_card_names + listed_cards

    exclusion_clause= "CardType NOT REGEXP \'{0}\' AND CardName NOT REGEXP \'{1}\' AND Rules NOT REGEXP \'{2}\'".format(
        "|".join(unrandomized_card_types), "|".join(none_of_these_cards), unrandomized_card_rules)
    return exclusion_clause