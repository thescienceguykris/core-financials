import financials.models as models
import financials.common.util as util
import requests

def getLoginUrl( settings, state ):
    auth_url = "https://auth.monzo.com/?client_id={0}&redirect_uri={1}&response_type=code&state={2}"
    client_id = settings['client-id']
    redirect_uri = settings['redirect-url']

    return auth_url.format( client_id, redirect_uri, state )

def getAuthCode( settings, state, args ):
    code = args.get('code')
    returned_state = args.get('state')

    if returned_state != state:
        return "Invalid state returned.", 400

    if code == None:
        return "Invalid code returned.", 403

    req = requests.post(
        url = "https://api.monzo.com/oauth2/token",
        data = {
            "grant_type": "authorization_code",
            "client_id": settings['client-id'],
            "client_secret": settings['client-secret'],
            "redirect_uri": settings['redirect-url'],
            "code": code
        }
    )

    return req.json()

def saveAuthCode( db, auth_code ):
    access_token = models.access_tokens.tokens(
        access_token=auth_code.get("access_token"),
        refresh_token=auth_code.get("refresh_token"),
        client_id=auth_code.get("client_id"),
        user_id=auth_code.get("user_id"),
        expires_in=auth_code.get("expires_in")
    )

    db.session.add ( access_token ) 
    return db.session.commit()

def getAuthCodeFromDB():
    token = models.access_tokens.tokens.query.first()
    return token.access_token

def whoami(auth_code):
    return util.get_monzo_request( "/ping/whoami", auth_code= auth_code ).json()