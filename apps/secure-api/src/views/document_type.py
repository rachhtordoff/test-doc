from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


document_type = Blueprint('document_type', __name__)


#TODO
@document_type.route("/document_types/", methods=['GET'])
def search_documents():
    #call method to make the actual search
    results = Sql.get_all_types()
    result_dict = []
    for result in results:
        document_dict= result.to_dict()
        document_dict['status'] = []
        document_dict['uploaded'] = []
        document_dict['notes'] = []

        for status in result.documentstatus:
            document_dict['status'].append(status.to_dict())

        for doc in result.documentsuploaded:
            document_dict['uploaded'].append(doc.to_dict())

        for note in result.documentnotes:
            document_dict['notes'].append(note.to_dict())


        result_dict.append(document_dict)

    print(jsonify(result_dict))
    return jsonify(result_dict)

@document_type.route("/document_types/<user_id>", methods=['GET'])
def search_documents_user_id(user_id):
    #call method to make the actual search
    id=int(user_id)
    results = Sql.get_all_types()
    result_dict = []
    for result in results:
        document_dict= result.to_dict()
        document_dict['status'] = []
        document_dict['uploaded'] = []
        document_dict['notes'] = []


        for status in result.documentstatus:
            if status.user_id == id:
                document_dict['status'].append(status.to_dict())

        for doc in result.documentsuploaded:
            if doc.user_id == id:
                document_dict['uploaded'].append(doc.to_dict())

        for note in result.documentnotes:
            if note.user_id == id:
                document_dict['notes'].append(note.to_dict())


        result_dict.append(document_dict)

    print(jsonify(result_dict))
    return jsonify(result_dict)


#TODO
@document_type.route("/document_type/<id>", methods=['GET'])
def get_document(id):
    #call method to make the actual search
    results = Sql.get_type({"id":id})

    #build output to return to user
    return build_output(results)

def build_output(results):
    output = {}
    output['data'] = []
    for result in results:
        output['data'].append(result.to_dict())
    return jsonify(output)
