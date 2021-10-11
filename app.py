from flask import Flask
from flask_restful import Api
from decouple import config
from flask_jwt import JWT
from resources.station import Station,StationList


from security import authenticate, identity
from resources.user import UserRegister

app= Flask(__name__)
app.secret_key = config('SECRET_KEY','secret key for this application')
api = Api(app)

jwt  = JWT(app,authenticate,identity)




api.add_resource(Station,'/station/<string:name>')
api.add_resource(StationList,'/stations')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(port=5000,debug=True)