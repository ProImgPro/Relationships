from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from bson import ObjectId
import pymongo
from utils import parse_req
from marshmallow import fields
from user import UserRegister, User
from auth import Login, Logout
from flask_jwt_extended import JWTManager


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable=myclient['mydb']
mycol = mytable['infor']
mycol2 = mytable['user']


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/"

jwt = JWTManager(app)

app.secret_key = 'Yep'


api = Api(app)


class Employee(Resource):
    def post(self):
        param = {
            'FullName': fields.String(),
            'Age': fields.Number(),
            'Career': fields.String(),
            'Lesson': fields.String(),
            'Note': fields.String(),
            'relationship': fields.String()
        }
        try:
            json_data = parse_req(param)
            FullName = json_data.get('FullName', None)
            Age = json_data.get('Age', None)
            Career = json_data.get('Career', None)
            Lesson = json_data.get('Lesson', None)
            Note = json_data.get('Note', None)
            relationship = json_data.get('relationship', None)

        except :
            return jsonify("An error occurred when getting data !")
        temp = str(ObjectId())
        infor_query = {
            'person_id': temp,
            'FullName': FullName,
            'Age': Age,
            'Career': Career,
            'Lesson': Lesson,
            'Note': Note,
            'relationship': relationship
        }

        try:
            mycol.insert_one(infor_query)
            return jsonify("Add new infor successfully")
        except:
            return jsonify("An error occurred when inserting data")

    def get(self):
        persons = mycol.find({}, {'_id': 0,'person_id':0 })
        totals = persons.count()
        if persons is None:
            return jsonify("No Person !")
        results = []
        for person in persons:
            results.append(person)
        data = {
            'totals': totals,
            'result': results
        }
        return jsonify(data)

    def put(self):
        person_id = request.args.get('person_id', None)
        param = {
            'FullName': fields.String(),
            'Age': fields.Number(),
            'Career': fields.String(),
            'Lesson': fields.String(),
            'Note': fields.String(),
            'relationship': fields.String()
        }
        try:
            json_data = parse_req(param)
            FullName = json_data.get('FullName', None)
            Age = json_data.get('Age', None)
            Career = json_data.get('Career', None)
            Lesson = json_data.get('Lesson', None)
            Note = json_data.get('Note', None)
            relationship = json_data.get('relationship', None)
        except:
            return jsonify("An error occurred when getting data !")

        query = {
            'person_id': person_id
        }
        try:
            person = mycol.find_one(query)
        except:
            return jsonify('An error occurred when finding data')

        if person is None:
            return jsonify("Can't found person")
        query_new = {
            '$set': {
            'FullName': FullName,
            'Age': Age,
            'Lesson': Lesson,
            'Career': Career,
            'Note': Note,
            'relationship': relationship
            }
        }
        try:
            mycol.update_one(query, query_new)
            return jsonify("Update Successfully")
        except:
            return jsonify("An error occurred when updating data")

    def delete(self):
        person_id = request.args.get('person_id', None)
        query = {
          'person_id': person_id
        }
        try:
            find_person = mycol.find_one({}, {'person_id': 1})
            if find_person is None:
                return jsonify("Can't found person !")
        except:
            return jsonify("An error occurred when finding data")

        try:
            mycol.remove(query)
            return jsonify("Delete successfully !")
        except:
            return jsonify("An error delete person")


api.add_resource(Employee, '/employee')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






