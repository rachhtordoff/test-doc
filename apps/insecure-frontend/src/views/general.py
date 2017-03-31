from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app, flash
import json
import requests

# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__,
                    template_folder='templates')

@general.route("/")
@general.route("/homepage")
def homepage():
    pagetitle="Homepage"
    return render_template('pages/index.html', pagetitle=pagetitle)

@general.route("/register", methods=['GET'])
def register_page():
    pagetitle = "Register"
    return render_template('pages/register.html', pagetitle=pagetitle)

@general.route("/register", methods=['POST'])
def register_user():
    return redirect('User-home/' + str(user[0]['id']))

@general.route("/login", methods=['GET'])
def login_page():
    pagetitle = "Login"
    return render_template('pages/login.html', pagetitle=pagetitle)

@general.route("/login", methods=['POST'])
def login_user():
    #str(user[0]['id'])
    return redirect('user-home/1')
    
@general.route("/user-home/<id>",  methods=['GET'])
def user_home_page(id):
    username="sally"
    pagetitle= "%s's homepage" % username
    user="sally"
    return render_template('pages/homepage.html', pagetitle=pagetitle, user=user)

@general.route("/documents")
def documents_main():
    username="sally"
    pagetitle= "%s's documents" % username
    user="sally"
    return render_template('pages/documents.html', pagetitle=pagetitle, user=user)

@general.route("/messages")
def messages_main():
    username="sally"
    pagetitle= "%s's messages" % username
    user="sally"
    return render_template('pages/messages.html', pagetitle=pagetitle,user=user)

@general.route("/events")
def events_main():
    username="sally"
    pagetitle= "%s's events" % username
    user="sally"
    return render_template('pages/events.html', pagetitle=pagetitle, user=user)


@general.route("/logout")
def logout():
    #pop session
    return redirect("/homepage")



@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_list(),
        "commit": current_app.config["COMMIT"]
    }),  mimetype='application/json', status=200)
