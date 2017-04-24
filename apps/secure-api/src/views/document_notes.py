from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


document_notes = Blueprint('document_notes', __name__)

@document_notes.route("/document_note/", methods=['POST'])
def new_document_note():
    json_data = request.json
    results = Sql.new_document_note(json_data['data'])
    output = {}
    output['data'] = []
    for key in results:
        output['data'].append(key.to_dict())
    return jsonify(output)

#TODO
@document_notes.route("/document_notes/<user_id>", methods=['GET'])
def get_notes(user_id):
    print(user_id)
    #call method to make the actual search
    results = Sql.get_notes({"user_id":user_id})

    #build output to return to user
    return build_output(results)

#TODO
@document_notes.route("/document_notes/<id>", methods=['PUT'])
def update_document_notes(id):
    json_data = request.json

    #call method to inset the work item
    #results = Sql.update_document_status(id, json_data['data'])

    #build output to return to user
    return "build_output(results)"


def build_output(results):
    output = {}
    output['data'] = []
    for result in results:
        output['data'].append(result.to_dict())
    return jsonify(output)
