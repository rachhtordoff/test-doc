from flask import request, Blueprint, Response, jsonify
from flask import current_app
from src.sql import Sql
from src.exceptions import ApplicationError
import json
import boto
from boto.s3.key import Key
from src import config
from boto.exception import S3CreateError


keyId =config.aws_access_key_id
sKeyId= config.aws_secret_access_key
boto.config.add_section('s3')
boto.config.set('s3', 'use-sigv4', 'True')
boto.config.set('s3', 'host', 's3.eu-west-2.amazonaws.com')
# This is the blueprint object that gets registered into the app in blueprints.py.
documents = Blueprint('documents', __name__)

@documents.route("/create_bucket/<user_id>", methods=['POST'])
def new_bucket(user_id):
    bucketName=str(user_id) + "12345"
    try:
        conn = boto.connect_s3(keyId,sKeyId, host='s3.eu-west-2.amazonaws.com')
        send = conn.create_bucket(bucketName, headers=None, location='eu-west-2', policy=None)
    except Exception as e:
        print(e)
        return e
    else:
        bucket={}
        bucket['bucket_name']= bucketName
        bucket['user_id']= user_id
        Sql.new_bucket(bucket)
        output= {}
        output['data'] = []
        output['data'].append(bucketName)
        output['data'].append(user_id)
        return jsonify(output)

#TODO
@documents.route("/post_document/<bucket_id>/<type_id>", methods=['POST'])
def new_document(bucket_id, type_id):
    data = request.files.to_dict()
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucket = conn.get_bucket(bucket_id)
    new_doc_name={}
    for key, value in data.items():
        new_key = bucket.new_key(key)
        new_key.set_contents_from_file(value)
        new_doc_name['document_name']= key
        new_doc_name['user_id']= bucket_id[:-5]
        new_doc_name['document_type_id']= type_id
        Sql.new_document_name(new_doc_name)
    return "success"

#TODO
@documents.route("/get_documents/<bucket_id>", methods=['GET'])
def search_documents(bucket_id):
#Connect to S3
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucket = conn.get_bucket(bucket_id, validate=False)
    bucket_list = bucket.list()
    output = {}
    output['data'] = []
    for key in bucket_list:
        output['data'].append(key.name)
    return jsonify(output)

@documents.route("/get_buckets/", methods=['GET'])
def get_buckets():
#Connect to S3
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucket = Sql.get_all_buckets()
    output = {}
    output['data'] = []
    for key in bucket:

        output['data'].append(key.to_dict())
    return jsonify(output)

@documents.route("/get_bucket/<user_id>", methods=['GET'])
def get_bucket_by_user_id(user_id):
#Connect to S3
    bucket = Sql.get_bucket({"user_id":user_id})
    output = {}
    output['data'] = []
    for key in bucket:
        output['data'].append(key.to_dict())
    return jsonify(output)

#TODO
@documents.route("/get_document/<bucket_id>/<doc_name>", methods=['GET'])
def get_document(bucket_id, doc_name):
    #call method to make the actual search
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucketName =  str(bucket_id)
    bucket = conn.get_bucket(bucketName, validate=False)

    key = bucket.get_key(doc_name)
    url = key.generate_url(3600, query_auth=True, force_http=True)
    return url

@documents.route("/delete_document/<bucket_id>/<doc_name>", methods=['PUT'])
def delete_document(bucket_id, doc_name):
    #call method to make the actual search
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucketName =  str(bucket_id)
    bucket = conn.get_bucket(bucketName, validate=False)
    key = bucket.delete_key(doc_name)
    return "success"

def build_output(results):
    output = {}
    output['data'] = []
    for key in results:
        output['data'].append(key)
    return jsonify(output)
