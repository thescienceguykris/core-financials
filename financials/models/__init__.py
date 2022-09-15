from financials.common.app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

from financials.models import access_tokens