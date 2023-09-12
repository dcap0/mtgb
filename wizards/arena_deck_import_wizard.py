import sys
sys.path.append("..")
from wizards.local_data import *


def parse_deck_export_file(deck_file, format=Format.STANDARD) -> LocalDeck:
    deck_file = open(deck_file).read().strip()
    return parse_deck_str(deck_file)

def parse_deck_str(deck_str: str, format=Format.STANDARD) -> LocalDeck:
    deck_list = deck_str.strip().split('\n')
    deck = LocalDeck(format=format)
    for card_str in deck_list[1:]:
        name = card_name(card_str)
        deck.set_copies(name,card_copies(card_str))
        deck.append_card(
                LocalCard(
                    name,
                    card_set(card_str),
                    card_collector_number(card_str)
                )   
        )
    return deck


def card_copies(card: str) -> str:
    return card.split(" ")[0]

def card_name(card: str) -> str:
    name = ""
    for string in card.split(" ")[1:]:
        if '(' in string:
            break
        name += "{} ".format(string)
    return name.strip()

def card_set(card: str) -> str:
    set = ""
    for string in card.split(" ")[2:]:
        if '(' in string:
            set = string.replace('(','').replace(')','')
            break
    return set

def card_collector_number(card: str) -> str:
    return card.split(" ")[-1].strip()