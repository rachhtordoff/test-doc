from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
events = Blueprint('events', __name__)

#TODO
@events.route("/user/<user_id>/events/", methods=['POST'])
def new_events(user_id):
    json_data = request.json
    #call method to inset the work item
    json_data['data']['user_id'] = user_id
    results = Sql.new_event(json_data['data'])

    #build output to return to user
    return build_output(results)

#TODO
@events.route("/user/<user_id>/events/", methods=['GET'])
def search_events(user_id):
    #call method to make the actual search
    data = request.args.to_dict()
    data['user_id'] = user_id
    results = Sql.get_user_events(data)

    #build output to return to user
    return build_output(results)

#TODO
@events.route("/user/<user_id>/events/<events_id>", methods=['GET'])
def get_events(user_id, events_id):
    #call method to make the actual search
    results = Sql.get_user_events({"id":id})

    #build output to return to user
    return build_output(results)

#TODO
@events.route("/user/<user_id>/events/<events_id>", methods=['PUT'])
def update_events(user_id, events_id):
    json_data = request.json

    #call method to inset the work item
    results = Sql.update_user_events(id, json_data['data'])

    #build output to return to user
    return build_output(results)


def build_output(results):
    output = {}
    output['data'] = []
    for application in results:
        output['data'].append(application.to_dict())
    return jsonify(output)
