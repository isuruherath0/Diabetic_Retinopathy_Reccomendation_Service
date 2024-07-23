from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decimal import Decimal
import dotenvals


uri = dotenvals.MONGODB_URI


class MongoDbSingleton:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = MongoClient(uri , server_api=ServerApi('1'))
        return cls.__instance
    

def insert_user_data(document):


    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['userdata']


    collection.insert_one(document)


def get_user_data(userid):
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['userdata']

    document = collection.find_one({"_id": userid})

    if document:

        discount_factor = Decimal(document.get('discount_factor'))
        learning_rate = Decimal(document.get('learning_rate'))
        epsilon = float(document.get('epsilon'))
        episodes = int(document.get('episodes'))
        cum_q = Decimal(document.get('cum_q'))


        episodes = int(episodes)
        cum_q = float(cum_q)



        return discount_factor, learning_rate, epsilon, episodes, cum_q
    else:
        return None


def update_epsilon(userid, epsilon):
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['userdata']

    collection.update_one({"_id": userid}, {"$set": {"epsilon": epsilon}})


def update_cum_q(userid, cum_q):
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['userdata']

    collection.update_one({"_id": userid}, {"$set": {"cum_q": cum_q}})

def update_episodes(userid, episodes):
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['userdata']

    collection.update_one({"_id": userid}, {"$set": {"episodes": episodes}})


#insert action data
    
def insert_action_data(document):
    
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['actiondata']
      
    collection.insert_one(document)




#get all action data and return the action list in an array
    

def get_action_data():
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['actiondata']
        
    action_data = collection.find_one({"_id": "actiondata"})
        
    if action_data:
        action_list = action_data.get('action_list')
        return action_list
    else:
        return None
    



            
    