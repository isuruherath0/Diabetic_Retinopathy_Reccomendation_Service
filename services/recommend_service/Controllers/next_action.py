from services.recommend_service.value_manager import action_list_v3

def next_action () :

    actionarr = action_list_v3()

    new_value = max(actionarr) + 1

    return new_value 
