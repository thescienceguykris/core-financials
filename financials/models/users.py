from enum import unique
from financials.models import db
from sqlalchemy.orm import relationship


class user(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   firstName = db.Column( db.String(15) )
   lastName = db.Column(db.String(15) )
   username = db.Column( db.String(15), unique = True )
   userState = db.Column( db.String(128), unique = True )
   tokens = relationship("tokens", back_populates="belongs_to")
   bankAccounts = relationship("bank_account", back_populates="belongs_to")


   def __init__( self, firstName, lastName, username, userState = None):
      self.firstName = firstName
      self.lastName = lastName
      self.username = username
      self.userState = userState
   