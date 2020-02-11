from marshmallow import fields
from flask_restful import Resource
from utils import parse_req
from flask import jsonify
import pymongo
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_raw_jwt, jwt_required)
from bson import ObjectId
from datetime import timedelta
import redis
from werkzeug.security import safe_str_cmp


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable=myclient['mydb']
mycol = mytable['infor']
mycol2 = mytable['user']
mycol3 = mytable['token']

red = redis.StrictRedis(host='localhost')


ACCESS_EXPIRES =timedelta(days=30)
FRESH_EXPIRES = timedelta(days=30)
revoked_store = red


class Login(Resource):
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
            return jsonify("An error occurred when getting data !")

        user = mycol2.find_one({'username': username})

        if not safe_str_cmp(user['password'], password):
            print(user['password'])
            return jsonify("Your password is wrong !")

        access_token = create_access_token(identity=str(user['_id']), expires_delta=ACCESS_EXPIRES)
        fresh_token = create_refresh_token(identity=str(user['_id']), expires_delta=FRESH_EXPIRES)
        dict1 = {
            'access_token': access_token,
            'fresh_token': fresh_token,
            'message': 'Login successfully'
        }
        user_token = dict(
            _id=str(ObjectId()),
            person_id=user['_id'],
            access_token=access_token,
            fresh_token=fresh_token
        )
        mycol3.insert_one(user_token)
        if user['first_login'] is True:
            return jsonify(dict1)

        return jsonify(dict1)


class Logout(Resource):
    @jwt_required
    def delete(self):
        access_token = get_raw_jwt()
        mycol3.remove({'access_token': access_token})
        return jsonify("Logout successfully !")



