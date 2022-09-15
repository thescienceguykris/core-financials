import json

from financials.common.settings import settings
import financials.common.util as util
import financials.controller as controller

from flask import request, redirect
from financials.common.app import app
from financials.models import db

state = util.get_random_string(128)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login')
def login_url():
    return redirect( controller.getLoginUrl( settings, state ) )

@app.route('/login/callback')
def oauth_callback():
    args = request.args

    auth_code = controller.getAuthCode( settings, state, args )
    controller.saveAuthCode( db, auth_code )

    return auth_code

@app.route('/test/connection')
def test_connection():
    auth_code = controller.getAuthCodeFromDB()
    ping = controller.whoami(auth_code)
    return ping

@app.route('/accounts')
def accounts():
    auth_code = controller.getAuthCodeFromDB()
    accounts = controller.accounts( db, auth_code)
    return "OK", 200

app.run(host="0.0.0.0", debug=True)