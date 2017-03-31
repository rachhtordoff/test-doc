from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template,session
import json
import requests
from src import config
import requests

#checks if user has c
def new_user_setup(params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", config.SECURE_API_URL+ '/user_setup/', data=json.dumps(payload), headers=headers)
    resp =  json.loads(response.text)
    return resp

def new_user_account(params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", config.SECURE_API_URL+ '/user/', data=json.dumps(payload), headers=headers)
    resp =  json.loads(response.text)
    return resp

def create_user_bucket(id):
    user_id=str(id)
    response = requests.request("POST", config.SECURE_API_URL + '/create_bucket/'+ user_id)
    return response

def get_user_setup(username, password):
    resp = requests.get(config.SECURE_API_URL+ '/get_usersetup/?username=' + username + "&password=" + password)
    data = json.loads(resp.text)
    return data

def get_user_account(id):
    id= str(id)
    resp = requests.get(config.SECURE_API_URL + '/user/' + id)
    data = json.loads(resp.text)
    return data

def get_user_account_with_id(id):
    id= str(id)
    resp = requests.get(config.SECURE_API_URL + '/user_by_id/' + id)
    data = json.loads(resp.text)
    return data


def get_user_details_all(id):
    id= str(id)
    resp = requests.get(config.SECURE_API_URL + '/user_details/' + id)
    data = json.loads(resp.text)
    return data

def update_user_details(id, params):
    payload = {}
    payload['data'] = params
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("PUT", config.SECURE_API_URL + '/user/' + str(id), data=json.dumps(payload), headers=headers)
    resp =  json.loads(response.text)
    return resp

def getnewpropertyid(applicationid):
    applicationid=str(applicationid)
    payload = "{\n  \"data\": {\n  \t\"application_id\": "+ applicationid +"\n  }\n}"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", config.FACT_FIND_API_URL + '/property/', data=payload, headers=headers)
    resp =  json.loads(response.text)
    return resp

def updatefirsttime(applicantid, firstbool):
    applicantid=str(applicantid)
    firstbool=firstbool
    payload = "{\n  \"data\": {\n  \t\"first_time_buyer\" : "+ firstbool +"\n  }\n}"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("PUT", config.FACT_FIND_API_URL + '/applicant/'+ applicantid, data=payload, headers=headers)
    resp =  json.loads(response.text)
    return resp

def update_user(userid, params):
    applicationid=applicationid
    applicant1firsttime=applicant1firsttime
    propertybool="true"
    if propertybool is "true":
        payload = "{\n  \"data\": {\n  \t\"application_id\": \"11\"\n  }\n}"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.request("POST", config.FACT_FIND_API_URL + '/property/', data=payload, headers=headers)
        resp =  json.loads(response.text)
        return resp

def getApplicantsForApplication(applicant_id):
    resp = requests.get(config.FACT_FIND_API_URL + '/applicant/' + str(applicant_id))
    data = json.loads(resp.text)
    return data

def getNewAddressForApplicant(applicant_id):
    payload = {}
    payload['data'] = {}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", config.FACT_FIND_API_URL + '/applicant/' + str(applicant_id) + '/address/', data=json.dumps(payload), headers=headers)
    resp =  json.loads(response.text)
    return resp
