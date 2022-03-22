import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
cluster = MongoClient(os.getenv('MONGOCONNECT'))
pokedb = cluster["pokemon"]
pokecollection = pokedb["pokemon"]
wantcollection = pokedb["wants"]
havecollection = pokedb["haves"]

def getWants(userID):
    userWants = ""
    pipeline = [{'$lookup':
                {'from': 'pokemon',
                'localField': 'dexnum',
                'foreignField': 'NUMBER',
                'as': 'userwants'}},
               {'$unwind': '$userwants'},
               {'$match':
               {'discord_id': userID}}]
    for doc in (wantcollection.aggregate(pipeline)):
        if doc['shiny']:
            userWants += "shiny "
        userWants += doc['userwants']['NAME'] + ", "
    if len(userWants) > 2:
        userWants = userWants.rstrip(userWants[-1])
        userWants = userWants.rstrip(userWants[-1])
    return userWants

def getHaves(userID):
    userHaves = ""
    pipeline = [{'$lookup': {'from': 'pokemon', 'localField': 'dexnum', 'foreignField': 'NUMBER', 'as': 'userhaves'}}, {'$unwind': '$userhaves'}, {'$match': {'discord_id': userID}}]
    for doc in havecollection.aggregate(pipeline):
        userHaves += str(doc['number']) + " "
        if doc['shiny']:
            userHaves += "shiny "
        userHaves += doc['userhaves']['NAME'] + ", "
    if len(userHaves) > 2:
        userHaves = userHaves.rstrip(userHaves[-1])
        userHaves = userHaves.rstrip(userHaves[-1])
    return userHaves

def verify_pokemon_exists(pokemon):
    myquery = {"NAME": str.title(pokemon)}
    doccount = pokecollection.count_documents(myquery)
    if doccount == 0:
        return False
    elif doccount == 1:
        return True
    else:
        print("We got a problem here.")
    return False

def get_dex_number(pokemon):
    myquery = {"NAME": str.title(pokemon)}
    results = pokecollection.find(myquery)
    for result in results:
      dexnum = result["NUMBER"]
    return dexnum

def check_if_want_exists(discord_id, dexnum, shiny):
    query = {"discord_id": discord_id, "dexnum": dexnum, "shiny": shiny}
    if (wantcollection.count_documents(query)) == 0:
      return False
    return True

def check_if_have_exists(discord_id, dexnum, shiny):
    query = {"discord_id": discord_id, "dexnum": dexnum, "shiny": shiny}
    if havecollection.count_documents(query) == 0:
        return False
    return True

def add_want(discord_id, dexnum, shiny=False):
  post = {"discord_id": discord_id, "dexnum": dexnum, "shiny": shiny}
  wantcollection.insert_one(post)

def add_have(discord_id, dexnum, number, shiny=False):
    post = {"discord_id": discord_id, "dexnum": dexnum, "number": number, "shiny": shiny}
    havecollection.insert_one(post)

def update_have(discord_id, dexnum, number, shiny=False):
    filter = {'discord_id': discord_id, 'dexnum': dexnum, 'shiny': shiny}
    newValues = {"$set": {'number': number}}
    havecollection.update_one(filter, newValues)

def remove_want(discord_id, dexnum, shiny=False):
  post = {"discord_id": discord_id, "dexnum": dexnum, "shiny": shiny}
  wantcollection.delete_one(post)

def remove_have(discord_id, dexnum, shiny=False):
    post = {"discord_id": discord_id, "dexnum": dexnum, "shiny": shiny}
    havecollection.delete_one(post)