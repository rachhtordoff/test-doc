from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


document_notification = Blueprint('document_notification', __name__)

@document_notification.route("/document_notification/", methods=['POST'])
def new_document_notification():
    json_data = request.json
    results = Sql.new_document_notification(json_data['data'])
    output = {}
    output['data'] = []
    for key in results:
        output['data'].append(key.to_dict())
    return jsonify(output)

#TODO
@document_notification.route("/document_notification/", methods=['GET'])
def search_document_notification():
    #call method to make the actual search
    results = Sql.get_document_notification(request.args.to_dict())

    #build output to return to user
    return build_output(results)

#TODO
@document_notification.route("/document_notification/<user_id>", methods=['GET'])
def get_notification(user_id):
    print(user_id)
    #call method to make the actual search
    results = Sql.get_document_notification({"user_id":user_id})

    #build output to return to user
    return build_output(results)

#TODO
@document_notification.route("/document_notification/<id>", methods=['PUT'])
def update_document_notification(id):
    json_data = request.json

    #call method to inset the work item
    results = Sql.update_document_notification(id, json_data['data'])

    #build output to return to user
    return build_output(results)


def build_output(results):
    output = {}
    output['data'] = []
    for result in results:
        output['data'].append(result.to_dict())
    return jsonify(output)
