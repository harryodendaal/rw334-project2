from . import db
from flaskapp import app


class employeList(db.Model):
    __tablename__ = 'employee_list'
    eid = db.Column(db.Integer, primary_key=True, nullable=True)
    firstname = db.Column(db.String(31))
    lastname = db.Column(db.String(31))
    email_id = db.Column(db.String(31))
