from flask import request, Blueprint, Response, jsonify, json
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
user = Blueprint('user', __name__)


@user.route("/user_setup/", methods=['POST'])
def new_usersetup():
    json_data = request.json
    acceptable_parameters = [
                "id",
                "username",
                "password"
                ]

    for arg in json_data['data']:
        if arg not in acceptable_parameters:
            raise ApplicationError('invalid parameter', 616)

    #call method to inset the work item
    results = Sql.new_usersetup(json_data['data'])

    #build output to return to user
    return build_output(results)
    #build_output(results)


@user.route("/get_usersetup/", methods=['GET'])
def get_user_login():
    #list the parameters that should be searchable
    acceptable_parameters = [
        'username',
        'password',
        'id'
    ]
    #check that the user hasnt passed in any invalid parameters
    for arg in request.args:
        if arg not in acceptable_parameters:
            raise ApplicationError('invalid parameter', 616)

    #call method to make the actual search
    results = Sql.get_user_login(request.args.to_dict())

    #build output to return to user
    return build_output(results)

@user.route("/user/", methods=['POST'])
def new_user():
    json_data = request.json
    print(json_data)
    #call method to inset the work item
    results = Sql.new_user(json_data['data'])

    #build output to return to user
    return build_output(results)


#TODO
@user.route("/user/<id>", methods=['PUT'])
def update_application(id):
    json_data = request.json
    #call method to inset the work item
    results = Sql.update_user(id, json_data['data'])

    #build output to return to user
    return build_output(results)

#TODO
@user.route("/user/<id>", methods=['GET'])
def get_user(id):
    #call method to make the actual search
    results = Sql.get_user({"account_id":id})

    #build output to return to user
    return build_output(results)


@user.route("/user_by_id/<id>", methods=['GET'])
def get_user_by_id(id):
    #call method to make the actual search
    results = Sql.get_user({"id":id})

    #build output to return to user
    return build_output(results)


#TODO
@user.route("/user_details/<id>", methods=['GET'])
def get_all_user_details(id):
    #call method to make the actual search
    output = {}
    output['data'] = Sql.get_user_with_details_documents(request.args.to_dict({"id":id}))

    #build output to return to user
    return jsonify(output)



def build_output(results):
    output = {}
    output['data'] = []
    for user in results:
        user_dict = user.to_dict()

        output['data'].append(user_dict)

    return jsonify(output)
