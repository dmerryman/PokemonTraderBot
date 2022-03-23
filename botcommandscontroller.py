import Constants.ErrorMessages
import mongodbcontroller
import Controllers.formattingcontroller
#import discordcontroller

async def listWants(ctx, targetID):
    if targetID is None:
        await ctx.send(Constants.ErrorMessages.NO_USER_FOUND)
        return
    wants = mongodbcontroller.getWants(targetID)
    if wants != "":
        await ctx.send(wants)
    else:
        await ctx.send(Constants.ErrorMessages.NO_WANTS_FOUND)

async def listHaves(ctx, targetID):
    if targetID is None:
        await ctx.send(Constants.ErrorMessages.NO_USER_FOUND)
        return
    haves = mongodbcontroller.getHaves(targetID)
    if haves != "":
        await ctx.send(haves)
    else:
        await ctx.send(Constants.ErrorMessages.NO_HAVES_FOUND)

async def want(ctx, poke, primaryArg = "", secondaryArg = ""):
    #primaryArg will either be shiny, or region/form.
    #secondaryArg can only be region/form.
    shiny = str.lower(primaryArg) == "shiny"
    pokelookupname = poke
    if not shiny:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
        if str.lower(primaryArg) == "alolan" or str.lower(primaryArg) == "galarian":
            pokelookupname = str.lower(primaryArg) + " " + poke
    else:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
          pokelookupname = str.lower(secondaryArg) + " " + poke
    #Making sure pokemon exists.  
    pokemonExists = mongodbcontroller.verify_pokemon_exists(pokelookupname)
    if pokemonExists:
        dexnum = mongodbcontroller.get_dex_number(pokelookupname)
        printpokename = Controllers.formattingcontroller.get_print_poke_name(pokelookupname, shiny)
        #Making sure want does not already exist.
        if not mongodbcontroller.check_if_want_exists(ctx.author.id, dexnum, shiny):
            mongodbcontroller.add_want(ctx.author.id, dexnum, shiny)
            await ctx.send(printpokename + " added!")
        else:
            await ctx.send("You already want " + printpokename)
    elif not pokemonExists:
        await ctx.send(Constants.ErrorMessages.NO_POKEMON_FOUND)

async def have(ctx, poke, number, primaryArg = "", secondaryArg = ""):
    shiny = str.lower(primaryArg) == "shiny"
    pokelookupname = poke
    if not shiny:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
        if str.lower(primaryArg) == "alolan" or str.lower(primaryArg) == "galarian":
            pokelookupname = str.lower(primaryArg) + " " + poke
    else:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
    pokemonExists = mongodbcontroller.verify_pokemon_exists(pokelookupname)
    if pokemonExists:
        dexnum = mongodbcontroller.get_dex_number(pokelookupname)
        printpokename = Controllers.formattingcontroller.get_print_poke_name(pokelookupname, shiny)
        if not mongodbcontroller.check_if_have_exists(ctx.author.id, dexnum, shiny):
            mongodbcontroller.add_have(ctx.author.id, dexnum, number, shiny)
            await ctx.send(ctx.author.name + " has " + str(number) + " " + printpokename)
        else:
            #have exists, and we should update it.
            mongodbcontroller.update_have(ctx.author.id, dexnum, number, shiny)
            await ctx.send(ctx.author.name + " updated to " + str(number) + " " + printpokename)
    elif not pokemonExists:
        await ctx.send(Constants.ErrorMessages.NO_POKEMON_FOUND)

async def unwant(ctx, poke, primaryArg = "", secondaryArg = ""):
    shiny = str.lower(primaryArg) == "shiny"
    pokelookupname = poke
    if not shiny:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
        if str.lower(primaryArg) == "alolan" or str.lower(primaryArg) == "galarian":
            pokelookupname = str.lower(primaryArg) + " " + poke
    else:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
    pokemonExists = mongodbcontroller.verify_pokemon_exists(pokelookupname)
    if pokemonExists:
        dexnum = mongodbcontroller.get_dex_number(pokelookupname)
        printpokename = Controllers.formattingcontroller.get_print_poke_name(pokelookupname, shiny)
        if mongodbcontroller.check_if_want_exists(ctx.author.id, dexnum, shiny):
            mongodbcontroller.remove_want(ctx.author.id, dexnum, shiny)
            await ctx.send(printpokename + " removed from wants!")
        else:
            await ctx.send("You don't have " + printpokename + " in your wants.")
    elif not pokemonExists:
        await ctx.send(Constants.ErrorMessages.NO_POKEMON_FOUND)

async def unhave(ctx, poke, primaryArg = "", secondaryArg = ""):
    shiny = str.lower(primaryArg) == "shiny"
    pokelookupname = poke
    if not shiny:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
        if str.lower(primaryArg) == "alolan" or str.lower(primaryArg) == "galarian":
            pokelookupname = str.lower(primaryArg) + " " + poke
    else:
        if str.lower(secondaryArg) == "alolan" or str.lower(secondaryArg) == "galarian":
            pokelookupname = str.lower(secondaryArg) + " " + poke
    pokemonExists = mongodbcontroller.verify_pokemon_exists(pokelookupname)
    if pokemonExists:
        dexnum = mongodbcontroller.get_dex_number(pokelookupname)
        printpokename = Controllers.formattingcontroller.get_print_poke_name(pokelookupname, shiny)
        if mongodbcontroller.check_if_have_exists(ctx.author.id, dexnum, shiny):
            mongodbcontroller.remove_have(ctx.author.id, dexnum, shiny)
            await ctx.send(printpokename + " removed from haves!")
        else:
            await ctx.send("You don't have " + printpokename + " in your haves.")
    elif not pokemonExists:
        await ctx.send(Constants.ErrorMessages.NO_POKEMON_FOUND)

async def clearWants(ctx, userID):
    success = mongodbcontroller.clear_wants(userID)
    if (success):
        await ctx.send("Wants cleared.")
    else:
        await ctx.send("Wants are already empty.")

async def clearHaves(ctx, userID):
    success = mongodbcontroller.clear_haves(userID)
    if (success):
        await ctx.send("Haves cleared.")
    else:
        await ctx.send("Haves are already empty.")