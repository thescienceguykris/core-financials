from sqlalchemy.orm import relationship
from financials.models import db

class bank_account(db.Model):
   id = db.Column('account_id', db.Integer(), primary_key = True)
   monzo_account_id = db.Column(db.String(30))
   belongs_to_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
   belongs_to = relationship("user", back_populates="bankAccounts")
   transactions = relationship("transaction", back_populates="account")

   def __init__(self, monzo_account_id, belongs_to_id):
      self.monzo_account_id = monzo_account_id
      self.belongs_to_id = belongs_to_id