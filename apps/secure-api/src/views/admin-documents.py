from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


documents = Blueprint('admin_document', __name__)

@admin_document.route("/document_list/", methods=['POST'])
def new_list():
    json_data = request.json
    #call method to inset the work item
    results = Sql.new_document(json_data['data'])

    #build output to return to user
    return build_output(results)

#TODO
@admin_document.route("/document_list/", methods=['GET'])
def search_lists():
    #call method to make the actual search
    results = Sql.get_document(request.args.to_dict())

    #build output to return to user
    return build_output(results)

#TODO
@admin_document.route("/document_list/<id>", methods=['GET'])
def get_document(id):
    #call method to make the actual search
    results = Sql.get_document({"id":id})

    #build output to return to user
    return build_output(results)

#TODO
@admin_document.route("/document_list/<id>", methods=['PUT'])
def update_list(id):
    json_data = request.json

    #call method to inset the work item
    results = Sql.update_property(id, json_data['data'])

    #build output to return to user
    return build_output(results)


def build_output(results):
    output = {}
    output['data'] = []
    for application in results:
        output['data'].append(application.to_dict())
    return jsonify(output)
