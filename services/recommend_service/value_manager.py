from services.recommend_service.mongodb_service import get_all_action_data

state_list = [
    1, #Breakfast, Non-Vegetarian, high calorie
    2, #Lunch, Non-Vegetarian, high calorie
    3, #Dinner, Non-Vegetarian, high calorie
    4, #Breakfast, Vegetarian, high calorie
    5, #Lunch, Vegetarian, high calorie
    6, #Dinner, Vegetarian, high calorie
    7, #Breakfast, Non-Vegetarian, low calorie
    8, #Lunch, Non-Vegetarian, low calorie
    9, #Dinner, Non-Vegetarian, low calorie
    10, #Breakfast, Vegetarian, low calorie
    11, #Lunch, Vegetarian, low calorie
    12, #Dinner, Vegetarian, low calorie

]

action_list = [
    1, #Chick peas with coconut scrapes
    2, #Brown rice with TOFU , and carrot salad
    3, #Sweet potato and lunu miris salad
    4, #Brown beans with onion mixture
    5, #Egg White omelette  with bread
    6, #1 cup of brown rice with sausages and dahl curry
    7, #Vegetable- mixed noodles with salmon
    8, #String Hoppers and Chicken curry
    9, #Egg Hoppers
    10,#oats- meal
    11,#sweet corn soup with mint salad
    12, #Butter bean pasta with tomato sauce
    13, #lean Chicken and vegetable lettuce wraps
    14, #Spicy BBq pork
    15, #Rice, soya meat and potatoes
]


def action_list_v3():
    actiondoc = get_all_action_data()
    actionarr = []
    for action in actiondoc:
        actionarr.append(action.get('_id'))
    return actionarr

