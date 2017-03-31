from flask import request, Blueprint, Response, render_template, flash, redirect, jsonify, g, render_template, session
from flask import current_app
import json
import requests
from ..forms import InitialSetup, AboutMe, FinanceDetails, PropertyDetails
from .user_controller import get_user_account_with_id

# This is the blueprint object that gets registered into the app in blueprints.py.
messages = Blueprint('messages', __name__,
                    template_folder='templates')

@messages.route("/messages")
def messages_main():
    id=session['user_id']
    user_account = get_user_account_with_id(id)
    username= user_account['data'][0]['forname']
    pagetitle= "%s's messages" % username
    return render_template('pages/messages.html', pagetitle=pagetitle,user=user, user_account= user_account)
