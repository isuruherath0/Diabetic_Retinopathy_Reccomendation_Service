from flask import request, Blueprint ,jsonify
from services.recommend_service.recommend_service import choose_action , create_table, init_table, update_q , get_cum_q , choose_action_v2 ,init_table_v2 ,update_q_sarsa ,create_action ,get_all_actions , add_version , init_table_v3 ,add_expert_1_data ,choose_action_v3 ,add_action_v3
from services.recommend_service.state_manager import state_manager ,state_manager_v2
from services.recommend_service.action_manager import action_manager , action_manager_v2
from flask_cors import CORS, cross_origin


recommendation_api = Blueprint('recommendation_api', __name__)

#Get Reccmondation through state

@recommendation_api.route('/api/recommendations', methods=['GET'])
def recommendation():
    user_id = request.form.get('user_id')
    state = int(request.form.get('state'))

    print(state)

    #return invalid if missing fields
    if not user_id or not state:
        return {'error': 'Missing user_id or state parameter'}, 400

    #validate if state in an integer
    try:
        state = int(state)
    except ValueError:
        return {'error': 'State must be an integer'}, 400


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


    #return invalid if missing fields
    if not user_id or not state or not action or not reward:
        return {'error': 'Missing user_id, state, action or reward parameter'}, 400
    
    # Validate if state, action, and reward are integers
    try:
        state = int(state)
        action = int(action)
    except ValueError:
        return {'error': 'State, action, and reward must be integers'}, 400

    # print ('Update Q service called with params : ' + user_id + " " + state + " " + action + " " + reward )


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

    #return invalid if missing fields
    if not user_id or not vegetarian or not weight or not height or not exersize_level:
        return {'error': 'Missing user_id, vegetarian, weight, height or exersize_level parameter'}, 400
    
    try:
        vegetarian = int(vegetarian)
        weight = float(weight)  # Supports both int and float inputs
        height = float(height)
        exersize_level = int(exersize_level)
    except ValueError:
        return {'error': 'Invalid input types. Check if values are numbers'}, 400
    
    #check if vegetarian is either 0 or 1 
    if vegetarian not in [0, 1]:
        return {'error': 'Invalid vegetarian value. Vegetarian should be either 0 or 1'}, 400
    
    #check if weight is between 0 and 200
    if weight not in range(0, 201):
        return {'error': 'Invalid weight value. Weight should be between 0 and 200'}, 400
    
    #check if height is between 0 and 200
    if height not in range(0, 201):
        return {'error': 'Invalid height value. Height should be between 0 and 200'}, 400
    
    #check if exersize_level is between 0 and 1
    if exersize_level not in range(0, 3):
        return {'error': 'Invalid exersize_level value. Exersize_level should be between 0 and 2'}, 400
    


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
@cross_origin(supports_credentials=True)
def get_cum_reward():
    user_id = request.args.get('user_id')

    #return invalid if missing fields
    if not user_id:
        return {'error': 'Missing user_id parameter'}, 400

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

    #return invalid if missing fields
    if not user_id or not state:
        return {'error': 'Missing user_id or state parameter'}, 400
    
    # #return invalid if state is not an integer
    
    try:
        state = int(state)
    except ValueError:
        return {'error': 'State must be an integer'}, 400
    
    #return invalid if state is not between 1 and 12

    if state not in range(1, 13):
        return {'error': 'Invalid state value. State should be between 1 and 12'}, 400


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


    #return invalid if missing fields
    if not user_id or not vegetarian or not weight or not height or not exersize_level or not meal:
        return {'error': 'Missing user_id, vegetarian, weight, height, exersize_level or meal parameter'}, 400
    

    try:
        vegetarian = int(vegetarian)
        weight = float(weight)  # Supports both int and float inputs
        height = float(height)
        exersize_level = int(exersize_level)
        meal = int(meal)
    except ValueError:
        return {'error': 'Invalid input types. Check if values are numbers'}, 400

    #check if vegetarian is either 0 or 1
    if vegetarian not in [0, 1]:
        return {'error': 'Invalid vegetarian value. Vegetarian should be either 0 or 1'}, 400
    
    #check if weight is between 0 and 200
    if weight not in range(0, 201):
        return {'error': 'Invalid weight value. Weight should be between 0 and 200'}, 400
    
    #check if height is between 0 and 200
    if height not in range(0, 201):
        return {'error': 'Invalid height value. Height should be between 0 and 200'}, 400
    

    #check if exersize_level is between 0 and 1
    if exersize_level not in range(0, 3):
        return {'error': 'Invalid exersize_level value. Exersize_level should be between 0 and 2'}, 400
    
    #check if meal is between 0 and 2
    if meal not in range(0, 3):
        return {'error': 'Invalid meal value. Meal should be between 0 and 2'},

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
@cross_origin(supports_credentials=True)
def updateq_v2():
    user_id = request.args.get('user_id')
    state = request.args.get('state')
    action = request.args.get('action')
    reward = request.args.get('reward')

    #return invalid if missing fields
    if not user_id or not state or not action or not reward:
        return {'error': 'Missing user_id, state, action or reward parameter'}, 400
    

    try:
        state = int(state)
        action = int(action)
    except ValueError:
        return {'error': 'State and action must be integers'}, 400
    

    update_res = update_q_sarsa('qtable' + user_id, state, action, reward)
    print(update_res)

    return {
        'update Response' : update_res
    }


#add action values to the action table

@recommendation_api.route('/api/v2/recommendations/create_action', methods=['POST'])
def create_action_v2():
    data = request.get_json()
    
    action_no = data.get('action_no')
    action_name = data.get('action_name')
    ES_no_1 = data.get('ES_no_1')
    ES_no_2 = data.get('ES_no_2')
    action_no = int(action_no)
    

    create_res = create_action(action_no, action_name, ES_no_1, ES_no_2)
    print(create_res)

    return {
        'create Response' : create_res
    }

#Get all actions

@recommendation_api.route('/api/v2/recommendations/get_all_actions', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_actions_v2():
    actions = get_all_actions()
    print(actions)

    return jsonify({'actions': actions})


#v3 of the API

#insert version

@recommendation_api.route('/api/v3/recommendations/insert_version', methods=['POST'])
def insert_version_v3():
    
    
    version_no = request.args.get('version_no')
    states = request.args.get('states')
    actions = request.args.get('actions')


    #return invalid if missing fields
    if not version_no or not states or not actions:
        return {'error': 'Missing version_no, states or actions parameter'}, 400
    

    states = int(states)
    actions = int(actions)


    create_res = add_version(version_no, states, actions)
    print(create_res)

    return {
        'create Response' : create_res
    }


#Create  and initialize new user V3

@recommendation_api.route('/api/v3/recommendations/new_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def new_user_v3():
    user_id = request.args.get('user_id')
    create_res = create_table('qtable' + user_id)
    init_res = init_table_v3('qtable' + user_id)
    print(create_res)
    print(init_res)


    return {
        'create Response' : create_res,
        'initialize response ' : init_res
    }

#add expert 1 data

@recommendation_api.route('/api/v3/recommendations/add_expert_1', methods=['POST'])
def add_expert_1():
    data = request.get_json()
    
    state = data.get('state')
    actions = data.get('actions')
    
    state = int(state)

    create_res = add_expert_1_data(state, actions)
    print(create_res)

    return {
        'create Response' : create_res
    }


#Get Reccmondation through state V3

@recommendation_api.route('/api/v3/recommendations', methods=['GET'])
@cross_origin(supports_credentials=True)
def recommendation_v3():
    user_id = request.args.get('user_id')
    state = request.args.get('state')

    #return invalid if missing fields
    if not user_id or not state:
        return {'error': 'Missing user_id or state parameter'}, 400
    
    # Validate if state is an integer
    try:
        state = int(state)
    except ValueError:
        return {'error': 'State, action, and reward must be integers'}, 400
    
    #return invalid if state is not between 1 and 12

    if state not in range(1, 13):
        return {'error': 'Invalid state value. State should be between 1 and 12'}, 400


    action = choose_action_v3('qtable' + user_id, state)
    print(action)

    return  {
        'activity' : action
    }

#Get Reccmondation through parameters V2

@recommendation_api.route('/api/v3/recommendations/get', methods=['GET'])
@cross_origin(supports_credentials=True)
def getrecommendation_v3():
    user_id = request.args.get('user_id')
    vegetarian = request.args.get('vegetarian')
    weight = request.args.get('weight')
    height = request.args.get('height')
    exersize_level = request.args.get('exersize_level')
    meal = request.args.get('meal')

    #return invalid if missing fields
    if not user_id or not vegetarian or not weight or not height or not exersize_level or not meal:
        return {'error': 'Missing user_id, vegetarian, weight, height, exersize_level or meal parameter'}, 400
    
    try :
        vegetarian = int(vegetarian)
        weight = float(weight)  # Supports both int and float inputs
        height = float(height)
        exersize_level = int(exersize_level)
        meal = int(meal)
    except ValueError:
        return {'error': 'Invalid input types. Check if values are numbers'}, 400


    state = state_manager_v2(vegetarian, weight, height, exersize_level, meal)

    print(state)


    action = choose_action_v3('qtable' + user_id, state)
    print(action)

    recommendation = action_manager_v2(action)


    return  {
        'Recommended Meal ' : recommendation,
        'state' : state,
        'action' : action
    
    }



# Add new actions

@recommendation_api.route('/api/v3/recommendations/create_action', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_action_v3():
    data = request.get_json()
    
    action_name = data.get('action_name')
    states_array = data.get('states')

    create_res = add_action_v3(action_name, states_array)

    return create_res