from mtgsdk import Card, QueryBuilder
from enum import Enum
from typing import List, Dict

#Constants for image links to basic Lands (incase they aren't present in response from mtgsdk)
PLAINS = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=295&type=card'
SWAMP = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=278&type=card'
MOUNTAIN = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=291&type=card'
ISLAND = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=293&type=card'
FOREST = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=289&type=card'

def handle_lands(land_card: Card):
    '''Ensures the Card object has an image url.

    Matches against basic land names and sets a default image_url if there is none.

    Parameters
    ----------
    land_card : mtgsdk.Card
        Card object (Basic Land) to be checked for image_url
    
    '''
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
    '''
    Contains constant values for referencing mtgsdk.Card instance attributes.
    '''
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
        '''Checks a string to see if it is a valid mtgsdk.Card attribute
        
        Parameters
        ----------
        query : str
            The string to be matched agains the class attributes.

        Return
        ----------
        bool
            True if is a valid attribute. False otherwise.
        '''
        retval = False
        for param in cls:
            if query.lower() == param.value:
                retval = True
                break
        return retval
    
def get_mtgsdk_card_members() -> List[str]:
    '''Gets a list of attributes of an mtgsdk.Card instance.

    Returns
    ----------
    List[str]
        String list of all instance attributes of an mtgsdk.Card instance.
    '''
    card = dir(Card())
    members = []
    for member in card:
        if not callable(member) and not member.__contains__('__') and member != 'RESOURCE':
            members.append(member)
    return members

def purge_invalid_params(query_parameters: Dict[str,str]) -> Dict[str,str]:
    '''Removes unexpeceted parameters from user input.

    Matches parameters against CardParameters enum to ensure they are valid.

    Parameters
    ----------
    query_parameters : Dict[str,str]
        All of the user provided parameters after they have been mapped flag to arguments.

    Returns
    ----------
    Dict[str,str]
        Valid parameters mapped `name` of attribute to query param.

    '''
    ret_val = {}
    for key in query_parameters.keys():
        if CardParameters.is_valid(key):
            ret_val[key] = query_parameters[key]
    return ret_val

def extract_flags_and_params(argv: list) -> tuple[List[str],Dict[str,str]]:
    ''' Provides flags for data to return to the user.

    Parses user provided flags. Takes any that have the `--` substring

    Parameters
    ----------
    argv : list
        The entire argument list that was passed to the bot command.
    '''
    
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
    '''Generates a query for the mtgsdk with provided params.

    Takes the provided paramaters and maps them to the kwargs in the QueryBuilder's
    `.where()` method.

    Parameters
    ----------
    parameters : dict
        A mapping of mtgsdk.Card attribute name to user's desired values.
    '''
    query = QueryBuilder(Card)
    for k,v in parameters.items():
            query.where(**{k:v})
    return query.all()
