from .database import db
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model,UserMixin):
    __tablename__='Users'
    def get_id(self):
        return (self.user_id)
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(300),nullable=False)
    u_timestamp=db.Column(db.DateTime(timezone=True),default=datetime.utcnow())

class Trackers(db.Model):
    __tablename__='Trackers'
    tracker_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tracker_name=db.Column(db.String(100),unique=True,nullable=False)
    creator_id=db.Column(db.Integer,db.ForeignKey(Users.user_id),nullable=False)
    timestamp=db.Column(db.DateTime(timezone=True),default=datetime.utcnow())
    description=db.Column(db.String)
    type=db.Column(db.String,nullable=False)
    no_users=db.Column(db.Integer,nullable=False,default=0)

class Tasks(db.Model):
    __tablename__='Tasks'
    task_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    ttimestamp=db.Column(db.DateTime(timezone=True),default=datetime.utcnow())
    ttracker_id=db.Column(db.Integer,db.ForeignKey(Trackers.tracker_id),nullable=False)
    value=db.Column(db.String,nullable=False)
    note=db.Column(db.String)
    tuser_id=db.Column(db.Integer,db.ForeignKey(Users.user_id),nullable=False)