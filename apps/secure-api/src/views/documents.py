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

# This is the blueprint object that gets registered into the app in blueprints.py.
documents = Blueprint('documents', __name__)

@documents.route("/create_bucket/<user_id>", methods=['POST'])
def new_bucket(user_id):
#Connect to S3 with access credentials
    keyId =config.aws_access_key_id
    sKeyId= config.aws_secret_access_key
    bucketName=str(user_id) + "12345"
    print(bucketName)
    conn = boto.connect_s3(keyId,sKeyId)
    conn.create_bucket(bucketName, headers=None, location='eu-west-2', policy=None)
    return "hello"

#TODO
@documents.route("/post_document/<user_id>", methods=['POST'])
def new_document(user_id):

    data = request.files.to_dict()
    print(data)
    bucketName=str(user_id) + "12345"
    keyId =config.aws_access_key_id
    sKeyId= config.aws_secret_access_key
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucket = conn.get_bucket(bucketName)

    for key, value in data.items():
        new_key = bucket.new_key(key)
        new_key.set_contents_from_file(value)
    return "success"

#TODO
@documents.route("/get_documents/<user_id>", methods=['GET'])
def search_documents(user_id):
#Connect to S3
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucketName =  str(user_id) + "12345"
    print(bucketName)
    bucket = conn.get_bucket(bucketName, validate=False)
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
    bucket = conn.get_all_buckets()
    output = {}
    output['data'] = []
    for key in bucket:
        output['data'].append(key.name)
    return jsonify(output)

#TODO
@documents.route("/get_document/<bucket_id>/<doc_name>", methods=['GET'])
def get_document(bucket_id, doc_name):
    #call method to make the actual search
    conn = boto.connect_s3(keyId,sKeyId, is_secure=False,host='s3.eu-west-2.amazonaws.com')
    bucketName =  str(bucket_id) + "12345"
    bucket = conn.get_bucket(bucketName, validate=False)

    key = bucket.get_key(doc_name)
    url = key.generate_url(3600, query_auth=True, force_http=True)
    return url

def bucket_id_calc(id):
    return (str(id) + "12345")

def build_output(results):
    output = {}
    output['data'] = []
    for key in results:
        output['data'].append(key)
    return jsonify(output)
