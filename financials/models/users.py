from financials.models import db

class users(db.Model):
   id = db.Column('user_id', db.Integer, primary_key = True)
   