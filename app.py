from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from decouple import config
from flask_jwt import JWT,jwt_required

from security import authenticate, identity

app= Flask(__name__)
app.secret_key = config('SECRET_KEY','secret key for this application')
api = Api(app)

jwt  = JWT(app,authenticate,identity)

stations = []

class Station(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('value',
    type=int,
    required= True,
    help= 'Value should be included'
        )

    @jwt_required()
    def get(self,name):
        station = next(filter(lambda x : x['name'] == name, stations),None)
        return {'station':station}, 200 if station else 404

    def post(self,name):
        if next(filter(lambda x : x['name'] == name, stations),None) is not None:
            return {'message': "An station with name '{}'already exists.".format(name)} , 400
        data = Station.parser.parse_args()
        station = {'name':name,'value':data['value']}
        stations.append(station)
        return station, 201

    def delete(self,name):
        
        global stations
        station = next(filter(lambda x : x['name'] == name, stations),None)
        if station :
            stations = list(filter(lambda x: x['name'] != name , stations))
            return {'message': "Item delted - {}".format(name)} , 202
        else:
            return {'message': "station has not found - {}".format(name)} , 404

    def put(self,name):
        data = Station.parser.parse_args()

        station = next(filter(lambda x : x['name'] == name, stations),None)
        if station is None:
            station = {"name":name, "value":data['value']}
            stations.append(station)
        else:
            station.update(data)
        return station ,201


class StationList(Resource):
    def get(self):
        return {'stations':stations}


api.add_resource(Station,'/station/<string:name>')
api.add_resource(StationList,'/stations')

app.run(port=5000,debug=True)