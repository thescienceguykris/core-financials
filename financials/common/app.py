from flask import Flask
from financials.common.settings import settings

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = settings['db']
