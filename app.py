from flask import Flask
from recommendation_api import recommendation_api


app = Flask(__name__)

app.register_blueprint(recommendation_api)

@app.route('/')
def index():

    return 'API is working! ' 

if __name__ == '__main__':
    app.run(debug=True )
