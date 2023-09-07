import discord
from discord.ext import commands
from helpers import arena_deck_import_helper
import asyncio

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
    
@mtgb.command(name="file-data")
async def file_data(ctx):
    print("Received File Data")
    await ctx.channel.send("Received {}".format(ctx.message.attachments[0].filename))
    await ctx.channel.send("Processing\n~~~~~~~~~~")
    deck_str = (await ctx.message.attachments[0].read()).decode('utf-8')
    local_deck = arena_deck_import_helper.parse_deck_str(deck_str)
    card_list = local_deck.get_basic_card_list()
    for i in card_list:
        await ctx.channel.send(i)
    await ctx.channel.send("~~~~~~~~~~\nProcessing Complete!")
        


if __name__ == '__main__':
    token = open('token.txt').readline()
    mtgb.run(token = token)