import string

def cardImgLinker(cards):
    card_img_links = []
    for card in cards:
        card_img = "http://dominion.diehrstraits.com/scans/" + cardStringify(card['CardSet']) + "/" + cardStringify(card['CardName']) + ".jpg"
        card_img_links.append(card_img)
    return card_img_links

def cardStringify(card_text):
    return card_text.translate(None, string.punctuation).lower().replace(" ", "")