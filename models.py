from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

#user table
class users(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(255), nullable=False)
        surname = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False, unique = True )
        password = db.Column(db.String(255), nullable=False )
        username = db.Column(db.String(40), nullable=False, unique = True )
        profile_picture = db.Column(db.LargeBinary)
        user_role = db.Column(db.String(25))
        #add relationships

        """relationship with account history table"""
        user_history = db.relationship('account_history',backref='users', lazy=True )

        """relationship with report table"""
        user_report = db.relationship("report", backref='users', lazy =True)

        """relationship with report_comments table"""
        report_comment = db.relationship("report_comments", backref="users", lazy=True)

        """relationship with notice board"""
        notice = db.relationship("notice_board", backref="users", lazy=True)       

       


#account history table

class account_history(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         date_created = db.Column(db.DateTime, default=datetime.utcnow)
         description = db.Column(db.String(50))

         #add relationships
         user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'Cascade'))


#Report table

class report(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        referenceNo = db.Column(db.String(10), nullable =False)
        campus = db.Column(db.String(20), nullable =False)
        campusBlock = db.Column(db.String(5))
        department =  db.Column(db.String(35))
        roomNumber = db.Column(db.String(5))
        priorityOfIssue = db.Column(db.Integer)
        reporter =  db.Column(db.String(50))
        dateReported = db.Column(db.DateTime, default = datetime.utcnow)
        issueStatus = db.Column(db.String(20))
        reporterRole = db.Column(db.String(20))
        upvoteCount = db.Column(db.Integer)
        description = db.Column(db.String(255))
    
        #relationships here
        user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'Cascade'))

        """relationship with reports_comments table"""
        report_comment = db.relationship("report_comments", backref='report', lazy =True)
        #relationship here
        report_image = db.relationship("image", backref="report",lazy=True)


#images
class image(db.Model):
        id= db.Column(db.Integer, primary_key=True)
        issue_image=db.Column(db.LargeBinary, nullable=True)

#relationshps here
        report_id= db.Column(db.Integer, db.ForeignKey('report.id',ondelete = 'Cascade'))

        
#report comments
class report_comments(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        reportComment = db.Column(db.String(100))
        dateCommented = db.Column(db.DateTime, default = datetime.utcnow)
        
        #relationships here
        report_id = db.Column(db.Integer, db.ForeignKey('report.id', ondelete = 'Cascade'), nullable = False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'Cascade'))



#notice board table

class notice_board(db.Model):
        
        id = db.Column(db.Integer, primary_key=True)
        announcements = db.Column(db.String(255))
        datePosted =  db.Column(db.DateTime, default = datetime.utcnow)
        
        #relationships here
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
