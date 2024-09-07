from flask import Flask
from flask_cors import CORS, cross_origin
from recommendation_api import recommendation_api

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(recommendation_api)

@app.route('/')
@cross_origin()
def index():
    return 'API is working!'

if __name__ == '__main__':
    app.run(debug=True)
