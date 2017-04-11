from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app
import json
import requests
from ..forms import InitialSetup, AboutMe, FinanceDetails, PropertyDetails
from .user_controller import get_user_account_with_id
from werkzeug import secure_filename
from src import config
import urllib.request

# This is the blueprint object that gets registered into the app in blueprints.py.
documents = Blueprint('documents', __name__,
                    template_folder='templates')



@documents.route("/documents",  methods=['GET'])
def documents_main():
    if 'user_id' not in session:
        return 'session ended'
    else:
        id=session['user_id']
        pagetitle= "Client Buckets"
        user_buckets = get_all_user_buckets()
        bucket_dict = []
        for bucket in user_buckets['data']:
            username = get_user_account_with_id(bucket['user_id'])
            bucket_dict.append({'Client_name':username['data'][0]['forname'], 'bucket_name': bucket['bucket_name']})
        return render_template('pages/documents.html', pagetitle=pagetitle, user_buckets=bucket_dict)

@documents.route("/bucket/<bucket_name>",  methods=['GET'])
def get_buckets(bucket_name):
    if 'user_id' not in session:
        return 'session ended'
    else:
        id=session['user_id']
        bucket_id = (int(bucket_name))
        documents = get_documents(bucket_id)
        pagetitle= "%s's documents" % bucket_name
        return render_template('pages/user_documents.html', pagetitle=pagetitle, documents=documents, bucket_name=bucket_id)


@documents.route("/documents",  methods=['POST'])
def documents_upload():
   if request.method == 'POST':
      file = request.files['file']
      user_id= session['user_id']
      if file and allowed_file(file.filename):
        file_content = file.read()
        file_name = file.filename
        docs = post_document(user_id, file_content, file_name)
        if docs == 200:
            return redirect('/documents')
        else:"failed to upload"
      else:
        return "not a valid file type"

@documents.route("/download-document/<doc_name>/<bucket_name>",  methods=['GET'])
def download_document(doc_name, bucket_name):
    if 'user_id' not in session:
        return 'session ended'
    else:
        documents = get_document(bucket_name, doc_name)
        wrapper = """<html>
        <head>
        <h1>%s</h1>
        </head>
        <body><p>URL: <a href=\"%s\">%s</a></p></body>
        </html>"""
        whole = wrapper % (doc_name, documents, documents)
    return whole

@documents.route("/delete-document/<doc_name>/<bucket_name>",  methods=['POST'])
def delete_document(doc_name, bucket_name):
    if 'user_id' not in session:
        return 'session ended'
    else:
        documents = remove_document(bucket_name, doc_name)
        if documents == 200:
            return redirect('/bucket/' + bucket_name)
        else:
            return "not deleted"

def post_document(userid, file_content, file_name):
    user_id=str(userid)
    file_store = {file_name: file_content}
    r = requests.request("POST", config.SECURE_API_URL + '/post_document/'+ user_id,  files=file_store)
    return r.status_code

def get_documents(userid):
    user_id=str(userid)
    response = requests.get(config.SECURE_API_URL + '/get_documents/'+ user_id)
    data = json.loads(response.text)
    return data

def get_all_user_buckets():
    response = requests.get(config.SECURE_API_URL + '/get_buckets/')
    data = json.loads(response.text)
    return data

def get_document(bucket_id, doc_name):
    bucket_id=str(bucket_id)
    response = requests.get(config.SECURE_API_URL + '/get_document/' + bucket_id + '/' + doc_name)
    print(response.status_code)
    return response.text

def remove_document(bucket_name, doc_name):
    response = requests.put(config.SECURE_API_URL + '/delete_document/' + bucket_name + '/' + doc_name)
    print(response.status_code)
    return response.status_code


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS
