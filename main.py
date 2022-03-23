import os
import discord
import Constants.ErrorMessages
import botcommandscontroller
import discordcontroller
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from pymongo import MongoClient
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('PokemonTrader')
#my_secret = os.environ['PokemonTrader']
cluster = MongoClient(os.getenv('MONGOCONNECT'))

pokedb = cluster["pokemon"]
pokecollection = pokedb["pokemon"]
wantcollection = pokedb["wants"]
havecollection = pokedb["haves"]
intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='list_my_wants', help = 'lists your wants')
async def listMyWants(ctx):
    await botcommandscontroller.listWants(ctx, ctx.author.id)
  
@bot.command(name='list_my_haves', help = 'lists your haves')
async def listMyHaves(ctx):
    await botcommandscontroller.listHaves(ctx, ctx.author.id)

@bot.command(name='list_wants', help = 'lists another user\'s wants. Usage = "!list_wants <username>"')
async def listOthersWants(ctx, otherUser = ""):
    otherUserID = discordcontroller.getUserID(ctx, otherUser)
    if otherUserID is None:
        await ctx.send(Constants.ErrorMessages.NO_USER_FOUND)
    await botcommandscontroller.listWants(ctx, otherUserID)

@bot.command(name='list_haves', help = 'lists another user\'s haves. Usage = "!list_haves <username>"')
async def listOthersHaves(ctx, otherUser):
    otherUserID = discordcontroller.getUserID(ctx, otherUser)
    if otherUserID is None:
        await ctx.send(Constants.ErrorMessages.NO_USER_FOUND)
    await botcommandscontroller.listOthersHaves(ctx, otherUserID)

@bot.command(name='have', help='adds a Pokemon to your have list. Usage: "!have <pokemonname> <numberyouhave>" or "!have <pokemonname> <numberyouhave> shiny"')
async def have(ctx, *args):
    if len(args) > 1:
        try:
            number = int(args[0])
            if number <= 0:
                await ctx.send(Constants.ErrorMessages.INVALID_HAVE_NUM)
        except ValueError:
            await ctx.send(Constants.ErrorMessages.INVALID_TYPE_ARGUMENT)
            return
    if len(args) == 4:
        #shiny with secondaryarg
        await botcommandscontroller.have(ctx, args[3], number, args[1], args[2])
    elif len(args) == 3:
        #shiny OR secondaryarg
        await botcommandscontroller.have(ctx, args[2], number, args[1])
    elif len(args) == 2:
        #not shiny and no secondaryarg
        await botcommandscontroller.have(ctx, args[1], number)
    elif len(args) < 2:
        await ctx.send(Constants.ErrorMessages.INVALID_NUM_ARGUMENTS)
        return

@bot.command(name='want', help='adds a Pokemon to your want list. Usage: "!want <pokemonname>" or "!want <pokemonname> shiny" ')
async def want(ctx, *args):
    if len(args) == 3:
        await botcommandscontroller.want(ctx, args[2], args[0], args[1])
    elif len(args) == 2:
        await botcommandscontroller.want(ctx, args[1], args[0])
    elif len(args) == 1:
        await botcommandscontroller.want(ctx, args[0])
    else:
        await ctx.send(Constants.ErrorMessages.INVALID_NUM_ARGUMENTS)

@bot.command(name='unhave', help='removes a Pokemon from your have list. Usage: "!unhave <pokemonname>" or "!unhave <pokemonname> shiny" ')
async def unhave(ctx, *args):
    if len(args) == 3:
        await botcommandscontroller.unhave(ctx, args[2], args[0], args[1])
    elif len(args) == 2:
        await botcommandscontroller.unhave(ctx, args[1], args[0])
    elif len(args) == 1:
        await botcommandscontroller.unhave(ctx, args[0])
    elif len(args) == 0:
        await ctx.send(Constants.ErrorMessages.INVALID_NUM_ARGUMENTS)

@bot.command(name='unwant', help='removes a pokemon from your want list. Usage: "!unwant <pokemonname>" or "!unwant <pokemonname> shiny"')
async def unwant(ctx, *args):
    if len(args) == 3:
        await botcommandscontroller.unwant(ctx, args[2], args[0], args[1])
    elif len(args) == 2:
        await botcommandscontroller.unwant(ctx, args[1], args[0])
    elif len(args) == 1:
        await botcommandscontroller.unwant(ctx, args[0])
    else:
        await ctx.send(Constants.ErrorMessages.INVALID_NUM_ARGUMENTS)

@bot.command(name='clear_wants', help='Clears your wants.')
async def clearwants(ctx, *args):
    await botcommandscontroller.clearWants(ctx, ctx.author.id)

@bot.command(name='clear_haves', help='Clears your haves.')
async def clearhaves(ctx, *args):
    await botcommandscontroller.clearHaves(ctx, ctx.author.id)
  
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return 
    raise error


keep_alive()

bot.run(TOKEN)
