card_type = "CardType NOT REGEXP 'Knight|Shelter|Ruins|Prize|Event'"

card_name = "CardName NOT REGEXP 'Spoils|Madman|Mercenary|Colony|Platinum|Potion'"

card_rules = "Rules NOT REGEXP 'This is not in the Supply'"

not_stuff = card_type + " AND " + card_name + " AND " + card_rules