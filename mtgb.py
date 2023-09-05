import discord
from discord.ext import commands
from helpers import arena_deck_import_helper

intents = discord.Intents.default()
intents.message_content = True
mtgb = commands.Bot(command_prefix='mtgb:', intents=intents)


@mtgb.command(name='test')
async def test(ctx):
    print("Received")
    channel = ctx.channel
    await ctx.send("Processing\n~~~~~~~~~~")
    local_deck = arena_deck_import_helper.parse_deck_export_file("PupperDeck.txt")
    deck = local_deck.get_basic_deck_data()
    for i in deck:
        await channel.send(i)
    await channel.send("~~~~~~~~~~\nProcessing Complete!")
    



if __name__ == '__main__':
    token = open('token.txt').readline()
    mtgb.run(token = token)