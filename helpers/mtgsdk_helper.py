from mtgsdk import Card

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