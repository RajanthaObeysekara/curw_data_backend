from sqlite3.dbapi2 import Cursor
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.station import StationModel

class Station(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('value',
    type=int,
    required= True,
    help= 'Value should be included'
        )

    @jwt_required()
    def get(self,name):
        station = StationModel.find_station_by_name(name)
        if station: 
            return station.json()
        return {"message":"station has not found"} , 400



    def post(self,name):
        station = StationModel.find_station_by_name(name)
        if station is not None:
            return {"message":"station is already exists"},400
        data = Station.parser.parse_args()
        station = StationModel(name,data['value'])

        try:
            station.station_insert()
        except:
            return {"message":"Internal Server Error"} , 500
        return  station.json() , 201

    


    def delete(self,name):
        if StationModel.find_station_by_name(name) is None:
            return {"message":"station is not exists"}
        connection = sqlite3.connect('data.db')
        cursor=connection.cursor()
        query= "DELETE FROM stations WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {"message": "Station has been deleted"} , 201        

    def put(self,name):
        data = Station.parser.parse_args() 
        station =StationModel.find_station_by_name(name)
        updated_station = StationModel(name,data['value'])
        if station is None:
            try:
                station.station_insert()
            except:
                return {"message":"internal server error"}, 500
        else:
            try:
                updated_station.station_update()
            except:
                return {"message":"internal server error"}, 500
        return updated_station.json()


class StationList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM stations" 
        result= cursor.execute(query)
        items = []

        for row in result:
            items.append({"name":row[0],"value":row[1]})

        connection.close()
        return {"stations":items}