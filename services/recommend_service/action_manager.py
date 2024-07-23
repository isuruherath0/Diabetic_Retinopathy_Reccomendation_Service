from services.recommend_service.mongodb_service import get_action_name


def action_manager(action):

    action = int(action)

    # return get_action_name(action)


    if action == 1:
        return "Rotti with lunu miris "
    elif action == 2:
        return "Brown rice with TOFU , and carrot salad"
    elif action == 3:
        return "Sweet potato and coconut scrapes" 
    elif action == 4:
        return "Brown beans with onion mixture "
    elif action == 5:
        return "Egg White omelette  with bread "
    elif action == 6:
        return "1 cup of brown rice with sausages and dahl curry "
    elif action == 7:
        return "Vegetable- mixed noodles with salmon "
    elif action == 8:
        return " String Hoppers and Chicken curry "
    elif action == 9:
        return "Egg Hoppers"
    elif action == 10:
        return " oats- meal"
    elif action == 11:
        return " sweet corn soup with mint salad"
    elif action == 12:
        return " Butter bean pasta with tomato sauce"
    elif action == 13:
        return "  lean Chicken and vegetable lettuce wraps"
    elif action == 14:
        return "  Spicy BBq pork"
    elif action == 15:
        return "  Rice, soya meat and potatoes"
    else:
        return "Invalid action"
    

