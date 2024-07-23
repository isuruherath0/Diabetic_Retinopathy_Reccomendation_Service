from services.recommend_service.mongodb_service import insert_user_data, get_user_data , update_epsilon , update_cum_q , update_episodes
from decimal import Decimal

def update_cumq(userid, reward):
    
    discount_factor, learning_rate, epsilon, episodes, cum_q = get_user_data(userid)


    tot_reward = cum_q * episodes

    tot_reward = Decimal(tot_reward)

    tot_reward = tot_reward + reward

    episodes = episodes + 1

    cum_q = tot_reward / episodes

    cum_q = float(cum_q)
    
    update_cum_q(userid, cum_q)
    update_episodes(userid, episodes)
    
    return cum_q