from services.recommend_service.mongodb_service import get_expert_1_data


def rule_based_reccomondation (state) :
    if state == 1:  # breakfast non veg high cal
        return [8,5 ,3 , 10]
    elif state == 2: #lunch non veg high cal
        return [6 , 14 , 13, 11]
    elif state == 3: #dinner non veg high cal
        return [7,8,6 ,15]
    elif state == 4: #breakfast veg high cal
        return [1,3,4]
    elif state == 5: #lunch veg high cal
        return [1,2 ,15]
    elif state == 6: #dinner veg high cal
        return [2 ,4 ,15]
    elif state == 7: #breakfast non veg low cal
        return [2,3,5 ,9]
    elif state == 8: #lunch non veg low cal
        return [6 ,13 ,1 ,11]
    elif state == 9: #dinner non veg low cal
        return [9,5 ,13 ,15]
    elif state == 10: #breakfast veg low cal
        return [1 , 5 ,11]
    elif state == 11: #lunch veg low cal
        return [2 , 11 ,15]
    elif state == 12: #dinner veg low cal
        return [2 , 12 , 15]
    else:
        return None
    

#rule_based_approach_for_reccomondation
    
def rule_based_approach_for_reccomondation (state):
    if state in (1,2,3):
        return [ 8 , 5 , 3 , 10 , 6 , 14 , 13, 11 , 7,8,6 ,15]  
    elif state in (4,5,6):
        return [1,3,4 ,1,2 ,15 ,2 ,4 ,15]
    elif state in (7,8,9):
        return [2,3,5 ,9 ,6 ,13 ,1 ,11 ,9,5 ,13 ,15]
    elif state in (10,11,12):
        return [1 , 5 ,11 ,2 , 11 ,15 ,2 , 12 , 15]
    

def rule_based_reccomondation_v3 (state) :

    actionarr = get_expert_1_data(state)

    return actionarr


#rule_based_approach_for_reccomondation
    
def rule_based_approach_for_reccomondation_v3 (state):

    actionarr = []

    if state in (1,2,3):

        actionarr = get_expert_1_data(1) + get_expert_1_data(2) + get_expert_1_data(3)

    elif state in (4,5,6):

        actionarr = get_expert_1_data(4) + get_expert_1_data(5) + get_expert_1_data(6)
        
    elif state in (7,8,9):

        actionarr = get_expert_1_data(7) + get_expert_1_data(8) + get_expert_1_data(9)

    elif state in (10,11,12):
        
        actionarr = get_expert_1_data(10) + get_expert_1_data(11) + get_expert_1_data(12)

    return actionarr
    