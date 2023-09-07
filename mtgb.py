import discord
from discord.ext import commands
from helpers import arena_deck_import_helper, mtgb_helper

intents = discord.Intents.default()
intents.message_content = True
mtgb = commands.Bot(command_prefix='mtgb:', intents=intents)


# @mtgb.command(name='test')
# async def test(ctx):
#     print("Received")
#     await ctx.channel.send("Processing\n~~~~~~~~~~")
#     local_deck = arena_deck_import_helper.parse_deck_export_file("PupperDeck.txt")
#     card_list = local_deck.get_basic_card_list()
#     for i in card_list:
#         await ctx.channel.send(i)
#     await ctx.channel.send("~~~~~~~~~~\nProcessing Complete!")
    
@mtgb.command(name="investigate-deck")
async def invesitgate_deck(ctx):
    print("Received deck file data")
    await ctx.channel.send("Received {}".format(ctx.message.attachments[0].filename))
    await ctx.channel.send("Processing")
    await ctx.channel.send('======')
    deck_str = (await ctx.message.attachments[0].read()).decode('utf-8')
    local_deck = arena_deck_import_helper.parse_deck_str(deck_str)
    card_list = local_deck.get_basic_card_list()
    for i in card_list:
        await ctx.channel.send(i)
        await ctx.channel.send('======')
    await ctx.channel.send('Complete')
    

@mtgb.command(name='get-card-data')
async def get_card_data(ctx, *args):
    print("Received card query")
    await ctx.channel.send("Querying")
    await ctx.channel.send('======')
    parameters = mtgb_helper.extract_flags_and_params(argv=list(args))
    return_list = parameters[0]
    cards = mtgb_helper.find_card(parameters[1])
    return_str = ""

    for card in cards:
        if len(return_list) == 0:
            return_list = ['name', 'mana_cost','type','image_url']

        for item  in return_list:
            return_str += "{}: {},\n".format(item.capitalize().replace('_',' '), card.__getattribute__(item))
        await ctx.channel.send(return_str[:-2])
        await ctx.channel.send('======')
    if len(cards) == 0:
        await ctx.channel.send('No Card Found. Please check parameters.')
        await ctx.channel.send('======')
    await ctx.channel.send('Complete')
    

        


if __name__ == '__main__':
    token = open('token.txt').readline()
    mtgb.run(token = token)