from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app
import json
import requests
from ..forms import InitialSetup, AboutMe, FinanceDetails, PropertyDetails
from .user_controller import get_user_account_with_id
from werkzeug import secure_filename
from src import config
import urllib.request
from json import dumps



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
        client_id = (bucket_name [:-5])
        output = []
        document_types = {}
        get_types = get_types_for_id(client_id)
        for type in get_types:
            document_types[type['document_type']] = (dict({"document_type": type['document_type']}))
            document_types[type['document_type']]['id'] = (dict({"id": type['id']}))
            document_types[type['document_type']]['user_id'] = []
            document_types[type['document_type']]['status'] = {}
            document_types[type['document_type']]['uploaded_doc'] = []
            document_types[type['document_type']]['doc_url'] = []
            document_types[type['document_type']]['notes'] = []


            status_store = type["status"]
            if not status_store:
                document_types[type['document_type']]['status'] = dict({"status" : " "})
            for status in status_store:
                if status['user_id'] == int(client_id):
                    document_types[type['document_type']]['user_id'].append(dict({"user_id": status['user_id']}))
                    document_types[type['document_type']]['status'] = (dict({"status" : status['status'], "id" : status['id']}))
            document_store = type['uploaded']
            for document in document_store:
                if document['user_id'] == int(client_id):
                    document_types[type['document_type']]['uploaded_doc'].append(dict({"doc_name": document['document_name']}))
                    documents = get_document(bucket_id,  document['document_name'])
                    document_types[type['document_type']]['doc_url'].append(dict({"url": documents}))
            note_store = type["notes"]
            for note in note_store:
                document_types[type['document_type']]['notes'].append(dict({"note": note}))
            output.append(document_types[type['document_type']])
        documents = get_documents(bucket_id)
        pagetitle= "%s's documents" % bucket_name
        return render_template('pages/user_documents.html', pagetitle=pagetitle, documents=documents, bucket_name=bucket_id, types=output)


@documents.route("/post-document",  methods=['POST'])
def documents_upload():
    if request.method == 'POST':
      file = request.files['file']
      bucket_name = request.form['bucket_name']
      document_type_id = request.form['type_id']
      if file and allowed_file(file.filename):
        file_content = file.read()
        file_name = file.filename
        docs = post_document(bucket_name, file_content, file_name, document_type_id)
        if docs == 200:
            return redirect('/bucket/' + bucket_name)
        else:"failed to upload"
      else:
        return "not a valid file type"

@documents.route("/post-status",  methods=['POST'])
def document_status():
    if request.method == 'POST':
        bucket_name = request.form['bucket_name']
        user_id =  bucket_name[:-5]
        status_dict = {}
        status_dict['document_type_id'] = request.form['documentid']
        if request.form['status'] != " ":
            status_dict['status'] = "Requested"
            status_dict['user_id'] = user_id
            id = request.form['status_id']
            update = update_status(id, status_dict)
        else:
            status_dict['status'] = "Requested"
            status_dict['user_id'] = user_id
            new =  new_status(status_dict)
    return redirect('/bucket/' + bucket_name)


@documents.route("/accept-doc",  methods=['POST'])
def document_accept():
    if request.method == 'POST':
        bucket_name = request.form['bucket_name']
        user_id =  bucket_name[:-5]
        status_dict = {}
        status_dict['document_type_id'] = request.form['type_id']
        status_dict['status'] = "Accepted"
        status_dict['user_id'] = user_id
        id = request.form['status_id']
        update = update_status(id, status_dict)
        print(status_dict)
    return redirect('/bucket/' + bucket_name)

@documents.route("/add-note",  methods=['POST'])
def add_note():
    if request.method == 'POST':
        bucket_name = request.form['bucket_name']
        user_id =  bucket_name[:-5]
        note_dict = {}
        note_dict['document_type_id'] = request.form['type_id']
        note_dict['note'] = request.form['note']
        note_dict['user_id'] = user_id
        update = new_note(note_dict)
        print(note_dict)
    return redirect('/bucket/' + bucket_name)

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

def post_document(bucket_id, file_content, file_name, type_id):
    file_store = {file_name: file_content}
    r = requests.post(config.SECURE_API_URL + '/post_document/'+ bucket_id + '/' + type_id,  files=file_store)
    return r.status_code

def get_documents(userid):
    user_id=str(userid)
    response = requests.get(config.SECURE_API_URL + '/get_documents/'+ user_id)
    data = json.loads(response.text)
    return data

def get_status(userid):
    user_id=str(userid)
    response = requests.get(config.SECURE_API_URL + '/document_status/'+ user_id)
    data = json.loads(response.text)
    print(data)
    return data

def update_status(userid, params):
    user_id=str(userid)
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(config.SECURE_API_URL + '/document_status/'+ user_id, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print(data)
    return data

def new_status(params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(config.SECURE_API_URL + '/document_status/', data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print("***")
    print(data)
    print("**")
    return data

def new_note(params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(config.SECURE_API_URL + '/document_note/', data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print("***")
    print(data)
    print("**")
    return data



def get_all_types():
    response = requests.get(config.SECURE_API_URL + '/document_types/')
    data = json.loads(response.text)
    return data

def get_types_for_id(user_id):
    response = requests.get(config.SECURE_API_URL + '/document_types/' + user_id)
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
