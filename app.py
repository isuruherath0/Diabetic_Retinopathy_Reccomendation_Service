from flask import Flask
from recommendation_api import recommendation_api
# from services.recommend_service.mongodb_service import get_action_from_version , update_action_from_version ,get_all_action_data ,get_expert_1_data


app = Flask(__name__)

app.register_blueprint(recommendation_api)

@app.route('/')
def index():

    return 'API is working! ' 

if __name__ == '__main__':
    app.run(debug=True )
