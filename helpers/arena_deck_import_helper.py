import sys
sys.path.append("..")
from helpers.local_data import *


def parse_deck_export_file(deck_data, format=Format.STANDARD) -> list:
    deck_file = open(deck_data).readlines()
    deck = LocalDeck(format=format)
    for card_str in deck_file[1:]:
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