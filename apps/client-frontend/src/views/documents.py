from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app
import json
import requests
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
        user_account = get_user_account_with_id(id)
        username= user_account['data'][0]['forname']
        pagetitle= "%s's documents" % username
        user="sally"
        get_bucket_id = get_bucket(id)
        bucket_id = get_bucket_id['data'][0]['bucket_name']
        gettypes = get_types(int(id))
        output=[]
        document_types = {}
        for type in gettypes:
            for status in type['status']:
                print(status)
                if status['status'] == "Requested":
                    document_types[type['document_type']] =(dict({"document_type": type}))
                    document_types[type['document_type']]['doc_url'] = []
                    document_types[type['document_type']]['notification'] = []
                    notifications_store = type["notification"]
                    print(notifications_store)
                    if not notifications_store:
                        document_types[type['document_type']]['notification'].append(({"bool" : " "}))
                    for notification in notifications_store:
                        document_types[type['document_type']]['notification'].append(dict({"bool" : notification['bool'], "id": notification['id']}))
                    for doc in type['uploaded']:
                        document_url = get_document(bucket_id,  doc['document_name'])
                        document_types[type['document_type']]['doc_url'].append(dict({doc['document_name']: document_url}))
                elif status['status'] == "Uploaded":
                    document_types[type['document_type']] =(dict({"document_type": type}))
                    document_types[type['document_type']]['doc_url'] = []
                    document_types[type['document_type']]['notification'] = []
                    notifications_store = type["notification"]
                    if not notifications_store:
                        document_types[type['document_type']]['notification'].append(dict({"bool" : " "}))
                    for notification in notifications_store:
                        document_types[type['document_type']]['notification'].append(dict({"bool" : notification['bool'], "id" : notification['id']}))
                    for doc in type['uploaded']:
                        document_url = get_document(bucket_id,  doc['document_name'])
                        document_types[type['document_type']]['doc_url'].append(dict({doc['document_name']: document_url}))
        output.append(document_types)
        return render_template('pages/documents.html', pagetitle=pagetitle, user=user, user_account= user_account, document=output, bucket_name=bucket_id)

@documents.route("/documents",  methods=['POST'])
def documents_upload():
   if request.method == 'POST':
      file = request.files['file']
      bucket_name = request.form['bucket_name']
      user_id = session['user_id']
      document_type_id = request.form['type_id']
      status_id = request.form['status_id']
      if file and allowed_file(file.filename):
        file_content = file.read()
        file_name = file.filename
        docs = post_document(bucket_name, file_content, file_name, document_type_id)
        if docs == 200:
            update_dict= {}
            update_dict['document_type_id'] = int(document_type_id)
            update_dict['status'] = "Uploaded"
            update_dict['user_id'] = user_id
            update_status(status_id, update_dict)
            notification_dict = {}
            notification_dict['document_type_id'] = document_type_id
            if request.form['notification'] != " ":
                notification_dict['bool'] = "true"
                notification_dict['user_id'] = user_id
                id = request.form['notification_id']
                update = update_notification(id, notification_dict)
            else:
                notification_dict['bool'] = "true"
                notification_dict['user_id'] = user_id
                new =  new_notification(notification_dict)
            return redirect('/documents')
        else:"failed to upload"
      else:
        return "not a valid file type"


@documents.route("/download-document/<doc_name>",  methods=['GET'])
def download_document(doc_name):
    if 'user_id' not in session:
        return 'session ended'
    else:
        user_id = session['user_id']
        get_bucket_id = get_bucket(user_id)
        bucket_id = get_bucket_id['data'][0]['bucket_name']
        documents = get_document(bucket_id, doc_name)
        wrapper = """<html>
        <head>
        <h1>%s </h1>
        </head>
        <body><p>URL: <a href=\"%s\">%s</a></p></body>
        </html>"""
        whole = wrapper % (doc_name, documents, documents)
        return whole


@documents.route("/add-note",  methods=['POST'])
def add_note():
    if request.method == 'POST':
        bucket_name = request.form['bucket_name']
        user_id =  bucket_name[:-5]
        note_dict = {}
        note_dict['document_type_id'] = request.form['type_id']
        note_dict['note'] = request.form['note']
        note_dict['user_id'] = user_id
        note_dict['type'] = "client"
        update = new_note(note_dict)
        print(note_dict)
        return redirect('/documents')

def post_document(userid, file_content, file_name, type_id):
    user_id=str(userid)
    file_store = {file_name: file_content}
    r = requests.post(config.SECURE_API_URL + '/post_document/'+ user_id + '/' + type_id,  files=file_store)
    print(r)
    return r.status_code

def update_status(id, params):
    status_id=str(id)
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(config.SECURE_API_URL + '/document_status/'+ status_id, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print(data)
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


def get_documents(userid):
    user_id=str(userid)
    response = requests.get(config.SECURE_API_URL + '/get_documents/'+ user_id)
    data = json.loads(response.text)
    return data

def get_types(userid):
    user_id=str(userid)
    response = requests.get(config.SECURE_API_URL + '/document_types/'+ user_id)
    data = json.loads(response.text)
    return data

def get_document(bucket_id, doc_name):
    bucket_id=str(bucket_id)
    response = requests.get(config.SECURE_API_URL + '/get_document/' + bucket_id + '/' + doc_name)
    print(response.status_code)
    return response.text

def update_notification(userid, params):
    user_id=str(userid)
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(config.SECURE_API_URL + '/document_notification/'+ user_id, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print(data)
    return data

def new_notification(params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(config.SECURE_API_URL + '/document_notification/', data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    print("***")
    print(data)
    print("**")
    return data


def get_bucket(user_id):
    user_id=str(user_id)
    response = requests.get(config.SECURE_API_URL + '/get_bucket/'+ user_id)
    data = json.loads(response.text)
    return data

def get_document(bucket_id, doc_name):
    bucket_id=str(bucket_id)
    response = requests.get(config.SECURE_API_URL + '/get_document/' + bucket_id + '/' + doc_name)
    #data = json.loads(response.text)
    return response.text

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS
