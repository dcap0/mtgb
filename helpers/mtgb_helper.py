from mtgsdk import Card, QueryBuilder
from enum import Enum
from typing import List, Dict
# from helpers.local_data import CardParameters

PLAINS = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=295&type=card'
SWAMP = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=278&type=card'
MOUNTAIN = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=291&type=card'
ISLAND = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=293&type=card'
FOREST = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=289&type=card'

def handle_lands(land_card: Card):
    match land_card.name:
        case "Forest":
            if land_card.image_url is None:
                land_card.image_url = FOREST
        case "Mountain":
            if land_card.image_url is None:
                land_card.image_url = MOUNTAIN
        case "Swamp":
            if land_card.image_url is None:
                land_card.image_url = SWAMP
        case "Island":
            if land_card.image_url is None:
                land_card.image_url = ISLAND
        case "Plains":
            if land_card.image_url is None:
                land_card.image_url = PLAINS
            
    return


class CardParameters(str,Enum):
    NAME ='name'
    MULTIVERSE_ID ='multiverse_id'
    LAYOUT ='layout'
    NAMES ='names'
    MANA_COST='mana_cost'
    CMC ='cmc'
    COLORS ='colors'
    COLOR_IDENTITY ='color_identity'
    TYPE ='type'
    SUPERTYPES ='supertypes'
    SUBTYPES ='subtypes'
    RARITY ='rarity'
    TEXT ='text'
    FLAVOR ='flavor'
    ARTIST ='artist'
    NUMBER ='number'
    POWER ='power'
    TOUGHNESS ='toughness'
    LOYALTY ='loyalty'
    VARIATIONS='variations'
    WATERMARK ='watermark'
    BORDER ='border'
    TIMESHIFTED ='timeshifted'
    HAND ='hand'
    LIFE ='life'
    RESERVED ='reserved'
    RELEASE_DATE ='release_date'
    STARTER ='starter'
    RULINGS ='rulings'
    FOREIGN_NAMES ='foreign_names'
    PRINTINGS ='printings'
    ORIGINAL_TEXT ='original_text'
    ORIGINAL_TYPE ='original_type'
    LEGALITIES ='legalities'
    SOURCE ='source'
    IMAGE_URL ='image_url'
    SET ='set'
    SET_NAME ='set_name'
    ID ='id'

    @classmethod
    def is_valid(cls, query: str) -> bool:
        retval = False
        for param in cls:
            if query.lower() == param.value:
                retval = True
                break
        return retval
    
def get_mtgsdk_card_members() -> List[str]:
    card = dir(Card())
    members = []
    for member in card:
        if not callable(member) and not member.__contains__('__') and member != 'RESOURCE':
            members.append(member)
    return members

def purge_invalid_params(query_parameters: Dict[str,str]) -> Dict[str,str]:
    ret_val = {}
    for key in query_parameters.keys():
        if CardParameters.is_valid(key):
            ret_val[key] = query_parameters[key]
    return ret_val

def extract_flags_and_params(argv: list) -> tuple[List[str],Dict[str,str]]:
    flags_to_values = {}
    return_card_values = []
    current_flag = ""
    for arg in argv:
        if '--' in arg:
            current_flag = arg.replace('--','')
            flags_to_values[current_flag] = ''
        else:
            if current_flag == 'return':
                return_card_values.append(arg)
            else:
                flags_to_values[current_flag] = arg

    return (return_card_values,purge_invalid_params(query_parameters=flags_to_values))

def find_card(parameters: dict) -> List[Card]:
    query = QueryBuilder(Card)
    for k,v in parameters.items():
            query.where(**{k:v})
    return query.all()
