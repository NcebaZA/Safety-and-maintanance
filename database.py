from models import *
from datetime import datetime

def create_user(first_name, surname, email, password,username, user_role):
    new_user = users(first_name=first_name,surname=surname,email=email,password=password,usernam=username,user_role=user_role)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return "An error has occured"
    return "Success"

def get_user(user_id):
    user = users.query.get(user_id)
    
    """returns user object if user exists"""
    if user:
        return user
    else:
        return "User does not exist"




def update_user(user_id):
    #upadates user info
    pass