from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


document_name = Blueprint('document_name', __name__)

@document_name.route("/document_name/", methods=['POST'])
def new_document_name():
    json_data = request.json
    bucket={}
    bucket['document_type_id']= '1'
    bucket['user_id']= '2'
    bucket['document_name'] = "rach_p60"
    #call method to inset the work item
    results = Sql.new_document_name(bucket)

    #build output to return to user
    return build_output(results)

#TODO
@document_name.route("/document_name/", methods=['GET'])
def search_documents():
    #call method to make the actual search
    results = Sql.new_document_name(request.args.to_dict())

    #build output to return to user
    return build_output(results)

#TODO
@document_name.route("/document_name/<id>", methods=['GET'])
def get_document(id):
    #call method to make the actual search
    results = Sql.get_document_name({"id":id})

    #build output to return to user
    return build_output(results)

#TODO
@document_name.route("/document_name/<id>", methods=['PUT'])
def update_document_name(id):
    json_data = request.json

    #call method to inset the work item
    results = Sql.update_document_name(id, json_data['data'])

    #build output to return to user
    return build_output(results)


def build_output(results):
    output = {}
    output['data'] = []
    for application in results:
        output['data'].append(application.to_dict())
    return jsonify(output)
