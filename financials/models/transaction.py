from sqlalchemy.orm import relationship
from financials.models import db

class transaction(db.Model):
   id = db.Column('transaction_id', db.Integer(), primary_key = True)
   account_id = db.Column(db.Integer(), db.ForeignKey("bank_account.account_id"))
   account = relationship("bank_account", back_populates="transactions")
   amount = db.Column(db.Integer())
   pending = db.Column(db.Boolean())
   spend_category = db.Column(db.String(30))
   description = db.Column(db.Text())
   monzo_transaction_id = db.Column(db.String(30))
   created = db.Column(db.DateTime())
   updated = db.Column(db.DateTime())
   settled = db.Column(db.DateTime())
   declined = db.Column(db.Boolean(), default=False)
   decline_reason = db.Column(db.String(30))
   

   def __init__(self, account_id, amount, pending, spend_category, description, monzo_transaction_id, created, declined=None, decline_reason=None, updated=None, settled=None):
      self.account_id = account_id
      self.amount = amount
      self.pending = pending
      self.spend_category = spend_category
      self.description = description
      self.monzo_transaction_id = monzo_transaction_id
      self.created = created
      self.updated = updated
      self.settled = settled
      self.declined = declined
      self.decline_reason = decline_reason