from flask_restful import Resource
from utils import parse_req
from flask import request, jsonify
import pymongo
from marshmallow import fields

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['mydb']
mycol1 = mytable['infor']
mycol2 = mytable['user']


class UserRegister(Resource):
    def post(self):
        param = {
            'username': fields.String(),
            'password': fields.String()
        }
        try:
            json_data = parse_req(param)
            username = json_data.get('username', None)
            password = json_data.get('password', None)
        except Exception:
            return jsonify("An error occurred when getting data")

        query_user = {
            'username': username,
            'password': password,
            'first_login': True
        }

        try:
            find_person = mycol2.find_one({'username': username})
            if find_person is not None:
                return jsonify("Username is already exist !")
            else:
                mycol2.insert_one(query_user)
                return jsonify('Register Successfully !')
        except Exception:
            return jsonify("An error occurred when inserting data !")


class User(Resource):

    def get(self):
        """"
            Function:Get all user with given status 0: 'Friend' , 1: 'Older', 2:'Younger'.
            Return: List of user, error message
        """
        relationship = request.args.get('status')
        query = {
            'relationship': relationship
        }
        try:
            user = list(mycol1.find(query, {'relationship': 1}))
            print(user)
            if user:
                return jsonify("Return successfully !")
            return jsonify("No data about this relationship !")
        except Exception:
            return jsonify("An error occurred when finding relationship !")




