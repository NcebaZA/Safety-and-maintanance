from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import flask_login
from random import randint


db = SQLAlchemy()



#user table
class users(db.Model,flask_login.UserMixin):

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(255), nullable=False)
        surname = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False, unique = True )
        password = db.Column(db.String(255), nullable=False )
        username = db.Column(db.String(40), nullable=False, unique = True )
        user_role = db.Column(db.String(25))
        confirmed = db.Column(db.Boolean, default=False)
        #add relationships

        """relationship with report table"""
        user_report = db.relationship("report", backref='users', lazy =True)

     

        """relationship with notice board"""
        notice = db.relationship("notice_board", backref="users", lazy=True)  

        """User functions to do stuff"""

        def is_confirmed(self):
                return self.confirmed
             





#Report table

class report(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.String(255))
        referenceNo = db.Column(db.String(10))
        campus = db.Column(db.String(20), nullable =False)
        campusBlock = db.Column(db.String(30))

        roomNumber = db.Column(db.String(5))
        priorityOfIssue = db.Column(db.Integer, default=0)
        reporter =  db.Column(db.String(50))
        dateReported = db.Column(db.DateTime, default = datetime.utcnow)
        issueStatus = db.Column(db.String(20), default="Pending")
        reporterRole = db.Column(db.String(20))
        
        def gen_ref(self):
                self.referenceNo = self.campus[0:2].upper() + "-" + self.campusBlock[0] + chr(randint(49,57)) + chr(randint(49,57)) + chr(randint(49,57)) + chr(randint(49,57))

        #relationships here
        user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'Cascade'))

      
        
        #relationship here
        report_image = db.relationship("image", backref="report",lazy=True)


#images
class image(db.Model):
        id= db.Column(db.Integer, primary_key=True)
        issue_image=db.Column(db.LargeBinary, nullable=True)

#relationshps here
        report_id= db.Column(db.Integer, db.ForeignKey('report.id',ondelete = 'Cascade'))

        


#notice board table

class notice_board(db.Model):
        
        id = db.Column(db.Integer, primary_key=True)
        announcements = db.Column(db.String(255))
        datePosted =  db.Column(db.DateTime, default = datetime.utcnow)
        
        #relationships here
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

