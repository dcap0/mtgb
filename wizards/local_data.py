from mtgsdk import Card
from wizards.mtgb_wizard import handle_lands
from enum import Enum



class Format(str,Enum):
    '''
    Enum handling constants for MTG formats.
    '''
    STANDARD = 'standard'
    COMMANDER = 'commander'
    DRAFT = 'draft'

#==========================================================================

class LocalCard:
    '''
    A class that represents a Magic the Gathering card for bot usage.

    ...

    Attributes
    ----------
    name : str
        The name of the card
    set : str
        The set the card belongs to
    collector_number : str
        The collector number of the card related to it's set.

    Methods
    ----------
    get_info(self) : str
        returns a string interpretation of the card's information.
    '''
    def __init__(self, name, set, collector_number):
        '''
        Parameters are the same as the class attributes. name, set, collector_number, image_url
        '''
        self.name = name
        self.set = set
        self.collector_number = collector_number
        self.card_image_urls = self.__get_card_image(name, set, collector_number)
        pass

    def get_info(self) -> str:
        '''returns a formatted string containing information about the card.'''
        return "Name: {}, Set: {}, Collector Number: {}, ImageUrl: {}".format(
            self.name,
            self.set,
            self.collector_number,
            self.card_image_urls
        )

    def __get_card_image(self, name, set, collector_number) -> []:
        '''Queries the mtgsdk and gets image data for the instance of the LocalCard'''
        image_urls = []
        card_data = Card.where(name=name).where(set=set).where(number=collector_number).all()
        for instance in card_data:
            handle_lands(instance)
            image_urls.append(instance.image_url)
        return image_urls


#==========================================================================

class LocalDeck:
    '''
    A class that represents a deck of cards, using LocalCard class.

    ...

    Attributes
    ----------
    format : str
        The deck format (ie. standard, commander, etc)
    cards: dict[LocalCard,int]
        The cards in the deck. A list of dicts, card to copies of card.

    Methods
    ----------
    append_card(card)
        Adds a card to the deck, increments number of copies of the card.

    set_copies(name, copies)
        Updates copies attribute with the name of the card 
        to the number of copies in the deck. 

    get_basic_card_list()
        Returns user readable list of strings formatted with basic card data.
    
    '''
    def __init__(self, format = Format.STANDARD):
        self.format = format
        self.copies = {} #name, copies
        self.cards = {} #name, cardobj
    
    def append_card(self, card: LocalCard):
        '''Adds a card to the deck, and increments the number of copies of the card.

        Parameters
        ==========
        card : LocalCard
            The card being added to the deck.
        '''
        self.cards[card.name] = card

    def set_copies(self, name: str, copies: int):
        '''Sets the number of copies of a card in a deck.

        Parameters
        ==========
        name : str
            Name of the card being added to the deck.

        copies: str
            String representation of the number of copies of the card deck.
        '''
        self.copies[name] = copies

    def get_basic_card_list(self) -> list:
        '''Gets basic card data for every card in the deck
        
        Iterates through LocalCards and gets attribute data. Format's it to a string
        for user readability.

        Returns
        ----------
        list
            A list of strings representing basic data for a card. Name, Copies, Image Urls.
        '''
        
        deck_data = []

        for k,v in self.copies.items():
            deck_data.append("{}, {}, {}".format(k,v,self.cards[k].card_image_urls))

        return deck_data
            



#==========================================================================
