from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

cluster = MongoClient(os.getenv('MONGOCONNECT'))

pokedb = cluster["pokemon"]
pokecollection = pokedb["pokemon"]
wantcollection = pokedb["wants"]
havecollection = pokedb["haves"]


def listOthersWantsTest():
    otherUserID = 228969602653224962
    wants = getWants(otherUserID)
    print(wants)


def getWants(userID):
    returnValue = ""
    pipeline = [{'$lookup':
                {'from': 'pokemon',
                'localField': 'dexnum',
                'foreignField': 'NUMBER',
                'as': 'userwants'}},
               {'$unwind': '$userwants'},
               {'$match':
               {'discord_id': userID}}]
    for doc in (wantcollection.aggregate(pipeline)):
      print(doc)
      returnValue += doc["NAME"] + " "
    return returnValue




listOthersWantsTest()