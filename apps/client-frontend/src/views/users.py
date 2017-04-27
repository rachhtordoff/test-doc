from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template,session
import json
import requests
from src import config
import requests
from .user_controller import new_user_setup, new_user_account, get_user_setup, get_user_account, get_user_account_with_id, update_user_details, create_user_bucket

# This is the blueprint object that gets registered into the app in blueprints.py.
users = Blueprint('users', __name__,
                    template_folder='templates')


@users.route("/")
@users.route("/homepage")
def homepage():
    pagetitle="Homepage"
    if 'user_id' in session:
        session.clear()
    return render_template('pages/index.html')

@users.route("/register", methods=['GET'])
def register_page():
    return render_template('pages/login.html')

@users.route("/register", methods=['POST'])
def register_user():
    #str(user[0]['id'])
    if request.method == 'POST':
        setup_data={}
        setup_data['username']= request.form['username']
        setup_data['password']= request.form['password']
        data= new_user_setup(setup_data)
        setup_id = data['data'][0]['id']
        account_id={}
        account_id['account_id']= setup_id
        account_id['complete']= "false"
        account = new_user_account(account_id)
        session['user_id'] = account['data'][0]['id']
        bucket_id = (int(account['data'][0]['id']))
        create_user_bucket(bucket_id)
        return redirect('account-setup/' + str(account['data'][0]['id']))

@users.route("/login", methods=['GET'])
def login_page():
    return render_template('pages/login.html')

@users.route("/login", methods=['POST'])
def login_user():
    #str(user[0]['id'])
    if request.method == 'POST':
        username  = request.form['username']
        password  = request.form['password']
    try:
        set_up = get_user_setup(username, password)
        user_account = get_user_account(set_up['data'][0]['id'])
        if user_account['data'][0]['type'] == 'client':
            if user_account['data'][0]['complete'] == 'false':
                session['user_id'] = user_account['data'][0]['id']
                return redirect('account-setup/' + str(user_account['data'][0]['id']))
            elif user_account['data'][0]['complete'] == 'true':
                session['user_id'] = user_account['data'][0]['id']
                return redirect('user-home/' + str(user_account['data'][0]['id']))
        else:
            return "You must me an administrator to log in to this service."
    except IndexError:
        return "no user found"

    except KeyError:
        return "Problem with service "

@users.route("/account-setup/<id>", methods=['GET'])
def account_setup_page(id):
    if 'user_id' not in session:
        return 'session ended'
    else:
        pagetitle = "Account Set-up"
        user_account = get_user_account_with_id(id)
        account_details = {}
        account_details['forname'] = user_account['data'][0]['forname']
        account_details['surname'] = user_account['data'][0]['surname']
        account_details['gender'] = user_account['data'][0]['gender']
        account_details['date_of_birth'] = user_account['data'][0]['date_of_birth']
        return render_template('pages/accountsetup.html', pagetitle=pagetitle, account_details=account_details)

@users.route("/account-setup", methods=['POST'])
def account_setup():
    if request.method == 'POST':
        user_id = session['user_id']
        gender  = request.form['gender']
        firstname =request.form['firstname']
        lastname =request.form['surname']
        dob= request.form['date_of_birth']
        update = {}
        update['forname'] = firstname
        update['surname'] = lastname
        update['gender'] = gender
        update['date_of_birth'] = dob
        update['complete'] =  'true'
        update['type'] =  'client'
        update_user_details(user_id, update)
        return redirect('user-home/' + str(user_id))
