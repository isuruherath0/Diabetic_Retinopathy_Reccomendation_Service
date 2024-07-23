from flask import request, Blueprint
from services.recommend_service.recommend_service import choose_action , create_table, init_table, update_q , get_cum_q , choose_action_v2 ,init_table_v2 ,update_q_sarsa
from services.recommend_service.state_manager import state_manager ,state_manager_v2
from services.recommend_service.action_manager import action_manager


recommendation_api = Blueprint('recommendation_api', __name__)

#Get Reccmondation through state

@recommendation_api.route('/api/recommendations', methods=['GET'])
def recommendation():
    user_id = request.form.get('user_id')
    state = int(request.form.get('state'))

    print(state)


    if state not in range(1, 4):
        return {'error': 'Invalid state value. State should be between 1 and 4'}, 400

    action = choose_action('qtable' + user_id, state)
    print(action)

    return  {
        'activity' : action
    }


#Create  and initialize new user

@recommendation_api.route('/api/recommendations/new_user', methods=['POST'])
def new_user():
    user_id = request.args.get('user_id')
    create_res = create_table('qtable' + user_id)
    init_res = init_table('qtable' + user_id)
    print(create_res)
    print(init_res)


    return {
        'create Response' : create_res,
        'initialize response ' : init_res
    }


#Update Q value

@recommendation_api.route('/api/recommendations/updateq', methods=['POST'])
def updateq():
    user_id = request.args.get('user_id')
    state = request.args.get('state')
    action = request.args.get('action')
    reward = request.args.get('reward')

    print ('Update Q service called with params : ' + user_id + " " + state + " " + action + " " + reward )


    update_res = update_q('qtable' + user_id, state, action, reward)
    print(update_res)

    return {
        'update Response' : update_res
    }
    

#get reccomondation through parameters

@recommendation_api.route('/api/recommendations/get', methods=['GET'])
def getrecommendation():
    user_id = request.args.get('user_id')
    vegetarian = request.args.get('vegetarian')
    weight = request.args.get('weight')
    height = request.args.get('height')
    exersize_level = request.args.get('exersize_level')

    print ("Finding state through state manager")

    state = state_manager(vegetarian, weight, height, exersize_level)

    print( 'State is :' +  str(state))

    print ('Calculating recccomondation ')


    action = choose_action('qtable' + user_id, state)
    print('State is :' +  str(action))

    print ('Showing reccomondation')

    recommendation = action_manager(action)


    return  {
        'Recommended Meal ' : recommendation,
        'state' : state,
        'action' : action
    
    }


#get cumulative reward

@recommendation_api.route('/api/recommendations/get_cum_reward', methods=['GET'])
def get_cum_reward():
    user_id = request.args.get('user_id')

    cum_q = get_cum_q('qtable' + user_id)
    
    return {
        
        'cumulative reward' : cum_q
    }


#Version 2 of the API

#Get Reccmondation through state V2

@recommendation_api.route('/api/v2/recommendations', methods=['GET'])
def recommendation_v2():
    user_id = request.args.get('user_id')
    state = request.args.get('state')
    action = choose_action_v2('qtable' + user_id, state)
    print(action)

    return  {
        'activity' : action
    }

#Get Reccmondation through parameters V2

@recommendation_api.route('/api/v2/recommendations/get', methods=['GET'])
def getrecommendation_v2():
    user_id = request.args.get('user_id')
    vegetarian = request.args.get('vegetarian')
    weight = request.args.get('weight')
    height = request.args.get('height')
    exersize_level = request.args.get('exersize_level')
    meal = request.args.get('meal')


    state = state_manager_v2(vegetarian, weight, height, exersize_level, meal)

    print(state)


    action = choose_action_v2('qtable' + user_id, state)
    print(action)

    recommendation = action_manager(action)


    return  {
        'Recommended Meal ' : recommendation,
        'state' : state,
        'action' : action
    
    }


#Create  and initialize new user V2

@recommendation_api.route('/api/v2/recommendations/new_user', methods=['POST'])
def new_user_v2():
    user_id = request.args.get('user_id')
    create_res = create_table('qtable' + user_id)
    init_res = init_table_v2('qtable' + user_id)
    print(create_res)
    print(init_res)


    return {
        'create Response' : create_res,
        'initialize response ' : init_res
    }

#Update Q value V2

@recommendation_api.route('/api/v2/recommendations/updateq', methods=['POST'])
def updateq_v2():
    user_id = request.args.get('user_id')
    state = request.args.get('state')
    action = request.args.get('action')
    reward = request.args.get('reward')
    update_res = update_q_sarsa('qtable' + user_id, state, action, reward)
    print(update_res)

    return {
        'update Response' : update_res
    }