from flask import Flask
from flask_restful import Api
from my_resource import PrivateResource

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

# add all resources here
api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
