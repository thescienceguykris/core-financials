import datetime
from typing_extensions import Required
from financials.models import db

class bank_account(db.Model):
   id = db.Column('account_id', db.Integer, primary_key = True)
   monzo_account_id = db.Column(db.String(30))

   def __init__(self, monzo_account_id):
      self.monzo_account_id = monzo_account_id