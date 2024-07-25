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




#get all action data when action _id is given
    

def get_action_data(action_id):
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['actiondata']
        
    action_data = collection.find_one({"_id": action_id})

        
    if action_data:
        name = action_data.get('action_name')
        es1 = action_data.get('expert_1')
        es2 = action_data.get('expert 2')
            
        return name , es1 , es2
    else:
        return None
    
# Get action name when action _id is given
    
def get_action_name(action_id):
        
        client = MongoDbSingleton.get_instance()
        db = client['research_RL']
        collection = db['actiondata']
        
        action_data = collection.find_one({"_id": action_id})
        
        if action_data:
            name = action_data.get('action_name')
            
            return name
        else:
            return None


#get all action data of all actions
        
def get_all_action_data():
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['actiondata']
        
    projection = {
        'action_no': 1,
        'action_name': 1,
        'expert_1': 1,
        'expert_2': 1
    }
    
    action_data = collection.find({}, projection)
    
    return list(action_data)
            
    

# Insert version data


def insert_version(document):

    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['version']

    collection.insert_one(document)



# get action value when version _id is given
    
def get_action_from_version(version_id):
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['version']
        
    version_data = collection.find_one({"_id": version_id})
        
    if version_data:
        action = version_data.get('actions')
            
        return action
    else:
        return None
    

# update action value when version _id is given and send response
    
def update_action_from_version(version_id, action):
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['version']


    collection.update_one({"_id": version_id}, {"$set": {"actions": action}})

    

#insert Expert_1 data
    
def insert_expert_1_data(document):

    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['expert_1']

    collection.insert_one(document)



#get action array when state _id is given
    
def get_expert_1_data(state_id):
        
    client = MongoDbSingleton.get_instance()
    db = client['research_RL']
    collection = db['expert_1']
        
    expert_1_data = collection.find_one({"_id": state_id})

    if expert_1_data:
        action_array = expert_1_data.get('action_array')
            
        return action_array
    
    else:
        return None

