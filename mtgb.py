import discord
from discord.ext import commands
from helpers import arena_deck_import_helper, mtgb_helper
import logging

intents = discord.Intents.default()
intents.message_content = True
mtgb = commands.Bot(command_prefix='mtgb:', intents=intents)
logging.basicConfig(
    filename = 'mtgb.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger('MTGB')

# @mtgb.command(name='test')
# async def test(ctx):
#     logger.info('Received')
#     await ctx.channel.send('Processing\n~~~~~~~~~~')
#     local_deck = arena_deck_import_helper.parse_deck_export_file('PupperDeck.txt')
#     card_list = local_deck.get_basic_card_list()
#     for i in card_list:
#         await ctx.channel.send(i)
#     await ctx.channel.send('~~~~~~~~~~\nProcessing Complete!')
    
@mtgb.command(
        name='investigate-deck',
        brief='Takes an export file from MTGA and returns count, name, and images',
        description='''
            Upload the text file exporter from Magic the Gathering, Arena as an attachment with the command.
            It will return your deck data for Counts and Names of card, an will provide Image Urls as well.
            (ex. With file attached, mtgb:investigate-deck)
        '''
    )
async def invesitgate_deck(ctx):
    '''Takes an MTG Arena Deck Export file and sends simple card data

    Parses the deck file and sends user data formatted:
    Name, Copies, Image Urls

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Message context received from Discord server.
    
    '''
    try:
        logger.info('Received deck file data')
        await ctx.channel.send('Received {}'.format(ctx.message.attachments[0].filename))
        await ctx.channel.send('Processing')
        await ctx.channel.send('======')
        deck_str = (await ctx.message.attachments[0].read()).decode('utf-8')
        local_deck = arena_deck_import_helper.parse_deck_str(deck_str)
        card_list = local_deck.get_basic_card_list()
        for i in card_list:
            await ctx.channel.send(i)
            await ctx.channel.send('======')
        await ctx.channel.send('Complete')
    except Exception:
        logger.exception('Exception in investigate_deck()',stack_info=True)
        await ctx.channel.send('Error Occured')

@mtgb.command(
        name='get-card-data',
        brief='Pass parameters regarding a card and receive basic data about the card in question.',
        description='''
            Run the command with flags using two dashes (--) and provide the search argument surrounded in quotes
            (ex. `mtgb:get-card-data --name "Black Lotus"` looks for the black lotus card)
            
            To return specific fields, use the `--return` flag and provide search arguments with no quotes seperated by spaces.
            (ex. `mtgb:get-card-data --name "Black Lotus" --return name type mana_cost text flavor` looks for the black lotus card and will send back everything listed.)

            No `--return` flag will default to name, mana_cost, type, text, and image_url
        '''
    )
async def get_card_data(ctx, *args):
    '''Takes user provided query params and returns card data.
    
    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Message context received from Discord server.
    *args : str
        Variable number of flags and parameters provided via Discord message 
    '''
    try:
        logger.info('Received card query')
        await ctx.channel.send('Querying')
        await ctx.channel.send('======')
        parameters = mtgb_helper.extract_flags_and_params(argv=list(args))
        return_list = parameters[0]
        cards = mtgb_helper.find_card(parameters[1])
        return_str = ''

        for card in cards:
            if len(return_list) == 0:
                return_list = ['name', 'mana_cost','type','text','image_url']

            for item  in return_list:
                return_str += '{}: {},\n'.format(item.capitalize().replace('_',' '), card.__getattribute__(item))
            await ctx.channel.send(return_str[:-2])
            await ctx.channel.send('======')
        if len(cards) == 0:
            await ctx.channel.send('No Card Found. Please check parameters.')
            await ctx.channel.send('======')
        await ctx.channel.send('Complete')
    except Exception:
        logger.exception('Exception in investigate_deck()',stack_info=True)
        await ctx.channel.send('Error Occured')
    

        


if __name__ == '__main__':
    logger.info('Starting MTGB')
    token = open('token.txt').readline()
    mtgb.run(token = token)