import sqlite3
from flask_restful import Resource,reqparse
from models.user import Usermodel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required= True,
        help='This feild is cannot be blank'
    )
    parser.add_argument('password',
        type=str,
        required= True,
        help='This feild is cannot be blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if Usermodel.find_by_username(data['username']):
            return {"message":"user already exists"},400
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (Null,?,?)"
            cursor.execute(query,(data['username'],data['password'],))
            connection.commit()
            connection.close()
            return {"message":"User has been successfully created."}, 201