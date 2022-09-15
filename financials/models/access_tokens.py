import datetime
from financials.models import db

class tokens(db.Model):
   id = db.Column('token_id', db.Integer, primary_key = True)
   access_token = db.Column(db.Text())
   refresh_token = db.Column(db.Text())
   client_id = db.Column(db.String(50))
   user_id = db.Column(db.String(50))
   expires_at = db.Column(db.DateTime())

   def __init__(self, access_token, refresh_token, client_id, user_id, expires_in):
      self.access_token = access_token
      self.refresh_token = refresh_token
      self.client_id = client_id
      self.user_id = user_id
      self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in*0.9)
