from decimal import Decimal
from services.recommend_service.dynamodb_service import create_Dynamo_table, init_dynamo_table, get_q_from_dynamo , get_action_with_max_q , update_q_value_in_q_table , init_dynamo_table_with_zero ,insert_new_rows_in_all_tables ,update_q_in_all_tables
from services.recommend_service.mongodb_service import insert_user_data, get_user_data , update_epsilon ,insert_action_data ,get_all_action_data , insert_version ,get_action_from_version , insert_expert_1_data ,update_expert_1_data ,get_expert_1_data
from services.recommend_service.reward_manager import update_cumq
from services.recommend_service.state_manager import next_state_calculator
from services.recommend_service.Controllers.rule_based import rule_based_reccomondation ,rule_based_approach_for_reccomondation ,rule_based_reccomondation_v3 ,rule_based_approach_for_reccomondation_v3
from services.recommend_service.value_manager import action_list , state_list ,action_list_v3
from services.recommend_service.Controllers.next_action import next_action
import numpy as np

def choose_action(table_name, state):

    print ('Choosing action with max Q value ' )

    action = get_action_with_max_q(table_name, state)
    return action

def choose_action_v2(table_name, state):

    userdata = get_user_data(table_name)

    episodes = userdata[3]
    episodes = int(episodes)
    state = int(state)
    print (episodes)

    if episodes < 10:   #EXPLORE

        if episodes < 4:
             action_set = rule_based_reccomondation(state)
        
        else :
            action_set = rule_based_approach_for_reccomondation(state)
   
        #get a random value from the action_set array

        action = action_set[np.random.randint(0, len(action_set))]

    else:  #EXPLOIT
        action = get_action_with_max_q(table_name, state)

    print(action)
    return action


def create_table(table_name):

    print('Creating table with name : ' + table_name)

    try:
        table = create_Dynamo_table(table_name)

        insert_user_data({
            "_id": table_name,
            "discount_factor": 0.5,
            "learning_rate": 0.5,
            "epsilon": 0.1,
            "episodes": 0,
            "cum_q": 0
        })



        table.wait_until_exists()

        print (' Q Table created via dynamoDb controller')
        print('User data created via mongoDb controller')
        response = {
            'status': 'success',
            'message': 'Table ' + table_name + ' created'
        }

    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response


    


def init_table(table_name):

    print('Initializing table with name : ' + table_name)

    try:
        table = init_dynamo_table(table_name)
        table.wait_until_exists()
        response = {
            'status': 'success',
            'message': 'Table ' + table_name + ' initialized'
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response

def init_table_v2(table_name):

    print('Initializing table with name : ' + table_name)

    try:
        table = init_dynamo_table_with_zero(table_name, state_list, action_list)
        table.wait_until_exists()
        response = {
            'status': 'success',
            'message': 'Table ' + table_name + ' initialized'
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response

def init_table_v3(table_name):

    print('Initializing table with name : ' + table_name)

    try:
        actionarr = action_list_v3()
        table = init_dynamo_table_with_zero(table_name, state_list, actionarr)
        table.wait_until_exists()
        response = {
            'status': 'success',
            'message': 'Table ' + table_name + ' initialized'
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response







def update_q(table_name, state, action, reward):
    curr_q = get_q_from_dynamo(table_name, state, action)
    learning_rate = Decimal('0.5')
    discount_factor = Decimal('0.5')
    reward_decimal = Decimal(reward.strip())

    print ('calculating new q value ')

    #Q(s,a) = Q(s,a) + alpha * (R(s,a) + gamma * maxQ(s',a') - Q(s,a)) - Q learning formula

    new_q = curr_q + learning_rate * (reward_decimal + discount_factor * curr_q - curr_q)

    if new_q < Decimal('0'):
        new_q = Decimal('0')
    elif new_q > Decimal('1'):
        new_q = Decimal('0.99')

    print ('updating q table with new q value')
    update_cumq(table_name, reward_decimal)
    response = update_q_value_in_q_table(table_name, state, action, new_q)


    return response


def update_q_sarsa(table_name, state, action, reward ):
    next_state = next_state_calculator(state)
    curr_q = get_q_from_dynamo(table_name, state, action)
    next_state = int(next_state)
    next_action = choose_action_v2(table_name, next_state)

    next_action = int(next_action)
    next_q = get_q_from_dynamo(table_name, next_state, next_action)
    learning_rate = Decimal('0.5')
    discount_factor = Decimal('0.5')
    reward_decimal = Decimal(reward.strip())

    print( 'next state : ' + str(next_state) + ' next action : ' + str(next_action) + ' next q : ' + str(next_q) + ' reward : ' + str(reward_decimal) + ' current q : ' + str(curr_q))
    print ('calculating new q value ')

     #Q(s,a) = Q(s,a) + alpha * (R(s,a) + gamma * maxQ(s',a') - Q(s,a)) - Q learning formula

    new_q = curr_q + learning_rate * (reward_decimal + discount_factor * next_q - curr_q)

    print ('updating q table with new q value')

    update_cumq(table_name, reward_decimal)

    response = update_q_value_in_q_table(table_name, state, action, new_q)

    return response


def get_cum_q(table_name):
    data = get_user_data(table_name)

    print(data)

    cum_q = data[4]

    return cum_q


#add action values to the action table

def create_action(action_no , action_name , ES_no_1 , ES_no_2):

    print('Creating  action table for action : ' + action_name)

    try:

        insert_action_data({
            "_id": action_no,
            "action_name": action_name,
            "expert_1": ES_no_1,
            "expert_2": ES_no_2
        })


        print('Action added')
        response = {
            'status': 'success',
            'message': 'Action Added'
        }

    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response


def get_all_actions():

    return get_all_action_data()


#insert version data to the version table

def add_version(version_no , states , actions):

    print('Creating  version table for version : ' + version_no)

    try:

        insert_version({
            "_id": version_no,
            "states": states,
            "actions": actions
        })


        print('Version added')
        response = {
            'status': 'success',
            'message': 'Version Added'
        }

    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    return response


#add expert 1 data to the expert 1 table


def add_expert_1_data(stateno , action_array):
    
        print('Creating  expert 1 table for state : ' + str(stateno))
    
        try:
    
            insert_expert_1_data({
                "_id": stateno,
                "action_array": action_array
            })
    
    
            print('Expert 1 data added')
            response = {
                'status': 'success',
                'message': 'Expert 1 data Added'
            }
    
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
        return response


#choose action v3

def choose_action_v3(table_name, state):

    userdata = get_user_data(table_name)

    episodes = userdata[3]
    episodes = int(episodes)
    state = int(state)
    print (episodes)

    if episodes < 10:   #EXPLORE

        if episodes < 4:
             action_set = rule_based_reccomondation_v3(state)
        
        else :
            action_set = rule_based_approach_for_reccomondation_v3(state)
   
        #get a random value from the action_set array

        action = action_set[np.random.randint(0, len(action_set))]

    else:  #EXPLOIT
        action = get_action_with_max_q(table_name, state)

    print(action)
    return action


#update array on expert table

def update_expert_1(stateno , action):

    current_array = get_expert_1_data(stateno)
    current_array.append(action)

    update_expert_1_data(stateno , current_array)




#add action v3

def add_action_v3(action_name , state_arrray):

    action_no = next_action()

    update_row_response = insert_new_rows_in_all_tables(state_list , action_no)

    for state in state_arrray:
        update_q_in_all_tables(state , action_no , Decimal('0.9'))

    print ('tables updated with new action')

    mongo_response = create_action(action_no , action_name , state_arrray , state_arrray)

    print('action created')

    for state in state_arrray:
        update_expert_1(state , action_no)

    print('expert system updated')

    return { 'update_row_response' : update_row_response , 'mongo_response' : mongo_response}

