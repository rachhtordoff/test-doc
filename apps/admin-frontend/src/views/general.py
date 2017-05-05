from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app, flash
import json
import requests
from .user_controller import new_user_setup, get_user_details_all, get_user_setup, get_user_account, get_user_account_with_id, update_user_details

# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__,
                    template_folder='templates')

@general.route("/user-home/<id>",  methods=['GET'])
def user_home_page(id):
    if id != str(session['user_id']):
        return "sorry- you cannot access this page!"
    else:
        user_account = get_user_account_with_id(id)
        username= user_account['data'][0]['forname']
        pagetitle= "%s's homepage" % username
        details = get_user_account_with_id(user_account['data'][0]['id'])
        return render_template('pages/homepage.html', pagetitle=pagetitle, details=details, user_account= user_account)

@general.route("/logout")
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect("/homepage")

@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_list(),
        "commit": current_app.config["COMMIT"]
    }),  mimetype='application/json', status=200)
