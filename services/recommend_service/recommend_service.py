from decimal import Decimal
from services.recommend_service.dynamodb_service import create_Dynamo_table, init_dynamo_table, get_q_from_dynamo , get_action_with_max_q , update_q_value_in_q_table , init_dynamo_table_with_zero
from services.recommend_service.mongodb_service import insert_user_data, get_user_data , update_epsilon 
from services.recommend_service.reward_manager import update_cumq
from services.recommend_service.state_manager import next_state_calculator
from services.recommend_service.Controllers.rule_based import rule_based_reccomondation ,rule_based_approach_for_reccomondation
from services.recommend_service.value_manager import action_list , state_list
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