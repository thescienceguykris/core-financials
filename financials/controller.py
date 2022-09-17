import financials.models as models
import financials.common.util as util
import requests
import datetime

def getLoginUrl( settings, state ):
    auth_url = "https://auth.monzo.com/?client_id={0}&redirect_uri={1}&response_type=code&state={2}"
    client_id = settings['client-id']
    redirect_uri = settings['redirect-url']

    return auth_url.format( client_id, redirect_uri, state )

def getAuthCode( settings, args ):
    code = args.get('code')

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

def saveAuthCode( db, current_user, auth_code ):
    access_token = models.tokens(
        access_token=auth_code.get("access_token"),
        refresh_token=auth_code.get("refresh_token"),
        client_id=auth_code.get("client_id"),
        user_id=auth_code.get("user_id"),
        expires_in=auth_code.get("expires_in"),
        belongs_to_id=current_user.id
    )

    db.session.add ( access_token ) 
    return db.session.commit()

def getAuthCodeFromDB( username ):
    user = models.user.query.filter_by(username=username).first()
    token = models.tokens.query.filter_by(belongs_to=user).order_by(models.tokens.expires_at.desc()).first()

    age_of_token:datetime.timedelta = datetime.datetime.now() - token.created_at

    if token == None:
        return (None, (False, False))

    return (token.access_token, (True, age_of_token.seconds < 300))

def doesUserExist( username ):
    current_user = models.user.query.filter_by(username=username).first()

    return current_user != None
    

def whoami( auth_code ):
    return util.get_monzo_request( "/ping/whoami", auth_code= auth_code ).json()

def accounts( db, username, auth_code ):
    current_user = models.user.query.filter_by(username=username).first()
    
    response = util.get_monzo_request( "/accounts", auth_code= auth_code ).json()
    accounts = response.get("accounts")

    if accounts == None:
        return response, 400

    for account in accounts:
        db.session.add(
            models.bank_account( account.get("id"), current_user.id )
        )
    
    db.session.commit()
    return True

def transactions( db, username, account_id, auth_code, younger_than_300 ):
    current_user = models.user.query.filter_by(username=username).first()
    account = models.bank_account.query.filter_by(id=account_id, belongs_to_id=current_user.id).first()

    if account == None:
        return "Invalid account", 400

    params = {
        "account_id": account.monzo_account_id
    }

    if not( younger_than_300 ):
        params["since"] = (datetime.datetime.now() - datetime.timedelta(days=89)).strftime("%Y-%m-%dT%H:%M:%SZ")

    response = util.get_monzo_request( "/transactions", auth_code=auth_code, params=params ).json()
    transactions = response.get("transactions")

    if transactions == None:
        return response, 400

    for transaction in transactions:
        
        try:
            created_date = datetime.datetime.strptime( transaction.get('created'), "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            created_date = datetime.datetime.strptime( transaction.get('created'), "%Y-%m-%dT%H:%M:%SZ")
                
        try:
            updated_date = datetime.datetime.strptime( transaction.get('updated'), "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            updated_date = datetime.datetime.strptime( transaction.get('updated'), "%Y-%m-%dT%H:%M:%SZ"),
        
        settled_date = None
        if transaction.get('settled') == None:
            settled_date = datetime.datetime.strptime( transaction.get('settled'), "%Y-%m-%dT%H:%M:%S.%fZ")

        # check whether record already exists
        update_session = db.session()

        existing_transaction = update_session.query(transaction).filter_by(
            models.transaction.monzo_transaction_id == transaction.get('id')
        ).first()

        if existing_transaction == None:
            db.session.add(
            models.transaction(
                account.id,
                transaction.get('amount'),
                transaction.get('amount_is_pending'),
                transaction.get('category'),
                transaction.get('description'),
                transaction.get('id'),
                created_date,
                transaction.get('decline_reason', None) != None,
                transaction.get('decline_reason'),
                updated_date,
                settled_date
            )
        )
    
        if (existing_transaction != None) and (existing_transaction.updated != updated_date):
            existing_transaction.update(
                amount=transaction.get('amount'),
                pending=transaction.get('amount_is_pending'),
                spend_category=transaction.get('category'),
                description=transaction.get('description'),
                delined=transaction.get('decline_reason', None) != None,
                decline_reason=transaction.get('decline_reason'),
                updated=updated_date,
                settled=settled_date
            )
            update_session.commit()

    db.session.commit()

    return transactions