import json

from financials.common.settings import settings
import financials.common.util as util
import financials.controller as controller

from flask import request, redirect
from financials.common.app import app
from financials.models import db, user

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<username>/login')
def login_url( username ):
    state = util.get_random_string(128)

    if not (controller.doesUserExist( username )):
        return "Unknown user", 300

    session = db.session()
    current_user = session.query(user).filter_by(username=username).first()
    current_user.userState = state
    session.commit()
    
    return redirect( controller.getLoginUrl( settings, state ) )

@app.route('/login/callback')
def oauth_callback():
    args = request.args
    returned_state = args.get('state')

    session = db.session()
    current_user = session.query(user).filter_by(userState=returned_state).first()
    
    if current_user == None:
        return "Invalid state returned.", 400

    auth_code = controller.getAuthCode( settings, args )
    controller.saveAuthCode( db, current_user, auth_code )

    return auth_code

@app.route('/<username>/test/connection')
def test_connection( username ):
    auth_code, success = controller.getAuthCodeFromDB( username )

    if not success:
        return "Invalid username", 403

    ping = controller.whoami(auth_code)
    return ping

@app.route('/<username>/accounts')
def accounts(username):
    auth_code, success = controller.getAuthCodeFromDB( username )

    if not success:
        return "Invalid username", 403

    accounts = controller.accounts( db, username, auth_code)
    return "OK", 200

app.run(host="0.0.0.0", debug=True)