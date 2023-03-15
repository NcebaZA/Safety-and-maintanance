from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import *
import flask_login

# testing by M Mngadi
from random import randint
# end testing


app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.login_view = "login"

#database config
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="bgoscsfb",
    dbpass="xOIQsgnH2fM5hLsfmVLT_UZbrdlPkD78",
    dbhost="isilo.db.elephantsql.com",
    dbname="bgoscsfb"
)
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisismyverysecretkey"

#initializing database to flask app
db.init_app(app)


#The line of code below is for performing database migrations 
migrate = Migrate(app, db)


#setting up login manager which is used for user authentication

login_manager.init_app(app)



@login_manager.user_loader
def user_loader(user_id):
     return users.query.get(int(user_id))



#HomePage route
@app.route("/")
def index():
   
    return "This the first page"


#This shows the login page for now. No login functionality has been added
@app.route("/login", methods=["GET","POST"])
def login():
     #if user is logged no need to show login page
       # """Login page code here"""
     if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_query = users.query.filter_by(email=email).first()

        print(f"email:{email}\npassword{password}")

        #Check if user exists
        if user_query :

            # if user exists check passowrd
           if user_query.password==password:
                
                next_page = request.args.get('next')
                
                flask_login.login_user(user_query)
                return redirect(next_page or url_for('admin'))
           
           #if password is incorrect then give error to user that password is incorrect

           elif user_query.password!=password:
            flash('Incorrect password')
                 
                 

            

            print(user_query)
        #if user doesn't exist then show an error   
        else:
              flash('Error user does not exist')
        
     return render_template("login.html")

@app.route("/logout")
def logout():
     flask_login.logout_user()
     return redirect(url_for("index"))

@app.route("/admin")
@flask_login.login_required
def admin():
    if flask_login.current_user.user_role=='admin':
        users_count = users.query.count()
        report_count = report.query.count()
        notices_count = notice_board.query.count()
        return render_template("/admin_screen/admin.html",users_count=users_count, report_count=report_count,notices_count=notices_count)
    else:
        
         return redirect(url_for("forbidden"))

@app.route("/admin/add_user", methods=["POST","GET"])
@flask_login.login_required
def add_user():
     if flask_login.current_user.user_role=='admin': 
        if request.method=="GET":
            return render_template("/admin_screen/add_user.html")
     #check if current logged in user has admin privilage and if so allow them to access the page
        elif  request.method=="POST":
          user_name = request.form.get("user_name")
          name = request.form.get("name")
          surname = request.form.get("surname")
          email = request.form.get("email")
          password = request.form.get("password")
          username = request.form.get("username")
          user_role = request.form.get("user_role")

          print(f"User Name:{user_name}\nName: {name}\nSurname: {surname}\nPassword:{password}\nUsername: {username}\nUser Role: {user_role}")
          
          #Check if user name or email has already been taken
          if users.query.filter_by(email=email).first() or users.query.filter_by(username=username).first():
              flash("Username or email already in use")
              return render_template("/admin_screen/add_user.html")
          
          
          #if it has not been taken then create a new user
          else:
            new_user = users(first_name=name, surname=surname, email=email,password=password, username=username,user_role=user_role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("admin"))
     else:
         redirect(url_for("forbidden"))

@app.route("/admin/users")
@flask_login.login_required
def show_users():
    if flask_login.current_user.user_role=='admin': 
        all_users = users.query.all()
        return render_template("/admin_screen/users.html", all_users=all_users)

#deleting users 
"""This is an endpoint for deleting users which takes in a argument of 'id' to delete a user"""
@app.route("/admin/users/delete")
@flask_login.login_required
def delete_user():
    #if request arguments exist delete user
    if request.args:
         user_id = request.args.get('id')
         print(user_id)
        
         user = users.query.filter_by(id=user_id).first()
         if user:
            db.session.delete(user)
            db.session.commit()

            return redirect(url_for("show_users"))
         else:
             flash("User does not exist")
             return redirect(url_for("show_users"))
         

#route for posting notices     
@app.route("/admin/notice", methods=["GET","POST"])
def add_notice():
    if flask_login.current_user.user_role=='admin':
        if request.method=="POST":
            user_id = flask_login.current_user.id
            announcement = request.form.get("announcement")
            new_notice = notice_board(announcements=announcement, user_id=user_id)
            db.session.add(new_notice)
            db.session.commit()
            flash("You successfully added a new notice")

            return redirect(url_for("add_notice"))

        else:
            return render_template("/admin_screen/add_notice.html")
    else:
        return "You do not have permission to access this page",403
    
@app.route("/admin/notices")
@flask_login.login_required
def show_notices():
    if flask_login.current_user.user_role=='admin': 
        if request.args:
            #delete notice here
            notice_id= request.args.get("delete")
            notice = notice_board.query.filter_by(id=notice_id).first()
            db.session.delete(notice)
            db.session.commit()

            return redirect(url_for("show_notices"))
            
        else:
            all_notices = notice_board.query.all()
            return render_template("/admin_screen/notices.html", all_notices=all_notices)
        


@app.route("/forbidden")
def forbidden():
     return render_template("/admin_screen/access_denied.html"),403

##The function below is a test of adding a user to the database table
@app.route("/create_user")
def create_user():
        new_user = users(first_name = "Nokthula", surname="Makhanya", email= "22023482@dut4life.ac.za", password="2023", username = "thuli012", user_role="admin")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

listUser=[]

#The function below is a test of gettinng all users from database table
@app.route("/get_users")
@flask_login.login_required
def get_users():
    all_users = users.query.all()
    for user in all_users:
          listUser.append(user.email)
          print(user)

    return f"These are users in the system {listUser}"


#This function takes user to forgot passsword page. NB: not functionality has been added 
@app.route("/forgot_password")
def forgot_password():
     return render_template("forgot-password1.html")

#This function takes user to issues table. NB: no functionality has been added
@app.route("/issues_table")
def show_issues_table():
     return render_template("issues_table.html")




#admin page route
"""You can add the admin page route here"""

#Report page route
"""Add report page route info here"""

reports=[]
@app.route("/add_report", methods=["GET","POST"])
def add_report():

    if request.method=="POST":
        type_of_issue = request.form.get("type_of_issue")
        campus =  request.form.get("campus")
        originator = request.form.get("originator")
        contact_details = request.form.get("contact_details")
        department = request.form.get("department")
        time_reported = request.form.get("time_reported")
        date_reported = request.form.get("date_reported")
        nature_of_work = request.form.get("nature_of_work")
        choose_file = request.form.get("choose_file")
        priority_of_work = request.form.get("priority_of_work")
        print(f"Type of issue:{type_of_issue}\nCampus {campus}\nOriginator {originator}\nContact Details{contact_details}\nDepartment{department}\nTime Reported{time_reported}\nDate Reported{date_reported}\nNature of work{nature_of_work}\nPriority of Work{priority_of_work}\nChoose File{choose_file}")
        #Connect to database
    return render_template("reportscreen.html")

reports=[]
@app.route("/add_report", methods=["GET","POST"])
def add_report():

    if request.method=="POST":
        type_of_issue = request.form.get("type_of_issue")
        campus =  request.form.get("campus")
        originator = request.form.get("originator")
        contact_details = request.form.get("contact_details")
        department = request.form.get("department")
        time_reported = request.form.get("time_reported")
        date_reported = request.form.get("date_reported")
        nature_of_work = request.form.get("nature_of_work")
        choose_file = request.form.get("choose_file")
        priority_of_work = request.form.get("priority_of_work")
        print(f"Type of issue:{type_of_issue}\nCampus {campus}\nOriginator {originator}\nContact Details{contact_details}\nDepartment{department}\nTime Reported{time_reported}\nDate Reported{date_reported}\nNature of work{nature_of_work}\nPriority of Work{priority_of_work}\nChoose File{choose_file}")
        #Connect to database
    return render_template("reportscreen.html")

if __name__ == "__main__":
    
    app.run(debug=True)
 