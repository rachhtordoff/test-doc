from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


document_status = Blueprint('document_status', __name__)

@document_status.route("/document_status/", methods=['POST'])
def new_document_name():
    json_data = request.json
    bucket={}
    bucket['document_type_id']= '1'
    bucket['user_id']= '3'
    bucket['status'] = "uploaded"
    print(bucket)
    results = Sql.new_document_status(bucket)
    output = {}
    output['data'] = []
    for key in results:
        output['data'].append(key.to_dict())
    return jsonify(output)

#TODO
@document_status.route("/document_status/", methods=['GET'])
def search_documents():
    #call method to make the actual search
    results = Sql.get_document_status(request.args.to_dict())

    #build output to return to user
    return build_output(results)

#TODO
@document_status.route("/document_status/<user_id>", methods=['GET'])
def get_document(user_id):
    print(user_id)
    #call method to make the actual search
    results = Sql.get_document_status({"user_id":user_id})

    #build output to return to user
    return build_output(results)

#TODO
@document_status.route("/document_status/<id>", methods=['PUT'])
def update_document_name(id):
    json_data = request.json

    #call method to inset the work item
    results = Sql.update_document_status(id, json_data['data'])

    #build output to return to user
    return build_output(results)


def build_output(results):
    output = {}
    output['data'] = []
    for result in results:
        output['data'].append(result.to_dict())
    return jsonify(output)
