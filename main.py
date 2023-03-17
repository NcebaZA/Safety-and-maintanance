import base64
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from models import *
import flask_login
from flask_login import current_user
from flask_mail import Mail, Message
from threading import Thread
import io
import os
# testing by M Mngadi
from random import randint
# end testing


app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.login_view = "login"

# database config
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode=require'.format(
    dbuser="maintenance_app",
    dbpass= os.environ.get('DBPASS'),
    dbhost="dpg-cg9rjokeoogm5ca5jvfg-a.frankfurt-postgres.render.com",
    dbname="maintenance"
)
print(database_uri)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME":os.environ.get('MAIL_USER') ,
    "MAIL_PASSWORD": os.environ.get('MAIL_PASS'),
    "MAIL_SUBJECT_PREFIX": 'Maintenance App'
}
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://maintenance_app:c0RtZ36Ja4y0XbhJx3aPb1htNO5PYVPB@dpg-cg9rjokeoogm5ca5jvfg-a.frankfurt-postgres.render.com/maintenance?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRETKEY')
app.config.update(mail_settings)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#initializing database to flask app
db.init_app(app)


#The line of code below is for performing database migrations 
migrate = Migrate(app, db)


#setting up login manager which is used for user authentication

login_manager.init_app(app)



@login_manager.user_loader
def user_loader(user_id):
     return users.query.get(int(user_id))


#The line of code below is for performing database migrations 
migrate = Migrate(app, db)


#setting up login manager which is used for user authentication

login_manager.init_app(app)




@login_manager.user_loader
def user_loader(user_id):
     return users.query.get(int(user_id))


# HomePage route
@app.route("/")
@app.route("/home")
def index():
    page=request.args.get("page",1,type=int)
    notices = notice_board.query.paginate(page=page,per_page=5)
    if notices:
        return render_template("/home_screen/Home_screen.html", pages=notices)
    return render_template("/home_screen/Home_screen.html")

#About us page route
@app.route("/about-us")
def about_us():

     return render_template("/home_screen/About.html")


# This shows the login page for now. No login functionality has been added
@app.route("/login", methods=["GET", "POST"])
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
                if flask_login.current_user.user_role=='admin':
                    return redirect(next_page or url_for('admin'))
                else:
                    return redirect(next_page or url_for("index"))
           
           #if password is incorrect then give error to user that password is incorrect

           elif user_query.password!=password:
            flash('Email or password is incorrect')
                 
                 

            

            print(user_query)
        #if user doesn't exist then show an error   
        else:
              flash('Email or password is incorrect')
        
     return render_template("login.html")

#sign up route
@app.route("/sign_up", methods=["POST","GET"])
def sign_up():

     if request.method == "POST":
          first_name =  request.form.get("first_name")
          surname = request.form.get("surname")
          username = request.form.get("username")
          email = request.form.get("email")
          password = request.form.get("password")
          confirm_password = request.form.get("confirm-password")
          print(first_name, surname, username, email, password, confirm_password)
      
      # process the sign-up data here
          #Check if user name or email has already been taken
          if users.query.filter_by(email=email).first() or users.query.filter_by(username=username).first():
               flash("Username or email already in use")
               return redirect(url_for("sign_up"))
               
          
          else:
               #check if password matches confirm passoword
               if password==confirm_password:
                #if it has not been taken then create a new user
                new_user = users(first_name=first_name, surname=surname, email=email,password=password, username = username, user_role = "user")
                db.session.add(new_user)
                db.session.commit()
                from send_email import sendtoken
                sendtoken(email=email)
                return redirect(url_for("login"))
               else:
                   flash("Error passwords do not match","not_match_password")
                   return redirect(url_for("sign_up"))
     else:
        # render the sign-up form here
         return render_template("/sign_up.html")


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
    else:

       return redirect(url_for("forbidden"))
    
#Update user info
@app.route("/admin/update-user/<id>", methods=["POST"])
@flask_login.login_required
def update_user_info(id):
    if current_user.user_role == 'admin':
        user = users.query.get(id)
        if user:
            user.user_role = request.form.get("user_role")
            print(f"{user.user_role}")
            db.session.commit()
            return redirect(url_for("show_users"))
        
    else:
       abort(403)

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
    else:
          flash("User does not exist")
          return redirect(url_for("index"))
         

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
        abort(403)
    
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
        
@app.route("/admin/update-notice/<id>", methods=["POST"])
@flask_login.login_required
def updateNotice(id):
    if flask_login.current_user.user_role=='admin':
        notice = notice_board.query.get(id)
        if notice:
            notice.announcements = request.form.get("editNotice")
            db.session.commit()
            flash("Successfully updated notice board", category="UpdateNoticeSuccess")
            return redirect(url_for("show_notices"))
        else:
            flash("Notice does not exist",category="updateNoticeError")
            return redirect(url_for("show_notices"))
        


@app.route("/forbidden")
def forbidden():
     return render_template("/admin_screen/access_denied.html"),403




# This function takes user to forgot passsword page. NB: not functionality has been added
@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot-password1.html")


# This function takes user to issues table.
@app.route("/issues_table", methods=['GET', 'POST'])
def show_issues():
    global gbl
    gbl = {}

    def append_args(link, d):
        for param in d:
            link += f"{param}={d[param]}"
            if list(d.keys())[-1]!=param:
                link += "&"
        return link

    def format_args(args):
        return args.split('+')

    def get_args_href(params):
        result = {}
        for item in params:
            t_args = params[item]
            arg_string = ''
            for obj in t_args:
                if t_args[-1]==obj:
                    arg_string+=obj
                else:
                    arg_string+=obj+'+'
            arg_string = arg_string.replace(' ', '%20').replace('+', '%2B')
            result[item]=arg_string
        return result

    def get_all_issues(argsPar={}):
        page = request.args.get('page', 1, type=int)
        keyword = request.args.get('keyword', '', type=str)
        campus = request.args.get('campus', '', type=str)
        block = request.args.get('block', '', type=str)
        priority = request.args.get('priority', '', type=str)

        main = {'cur_args': argsPar, 'pages': {}}

        if argsPar == {}:
            if keyword != '':
                main['cur_args']['keyword'] = format_args(keyword)

            if campus != '':
                main['cur_args']['campus'] = format_args(campus)

            if block != '':
                main['cur_args']['block'] = format_args(block)

            if priority != '':
                main['cur_args']['priority'] = format_args(priority)

            gbl['cur_args'] = main['cur_args']
        else:
            gbl['cur_args'] = argsPar

        filtered_data = None

        
        sql_query = 'SELECT * FROM report'

        if ('keyword' in main['cur_args'].keys()) or (
                'campus' in main['cur_args'].keys()) or (
                    'block' in main['cur_args'].keys()) or (
                        'priority' in main['cur_args'].keys()):
            sql_query += ' WHERE'

        if 'keyword' in main['cur_args'].keys():
            if main['cur_args']['keyword'] != ['']:
                sql_query += " ("
                for param in main['cur_args']['keyword']:
                    sql_query += f" report.\"referenceNo\" LIKE '{param}%'"
                sql_query += " )"

        if 'campus' in main['cur_args'].keys():
            if main['cur_args']['campus'] != ['']:
                if (sql_query[-1] == ")"):
                    sql_query += " AND"
                sql_query += " ("
                for param in main['cur_args']['campus']:
                    sql_query += f" report.\"campus\"='{param}'"
                    if param != main['cur_args']['campus'][-1]:
                        sql_query += ' OR'
                sql_query += " )"

        if 'block' in main['cur_args'].keys():
            if main['cur_args']['block'] != ['']:
                if (sql_query[-1] == ")"):
                    sql_query += " AND"
                sql_query += " ("
                for param in main['cur_args']['block']:
                    sql_query += f" report.\"campusBlock\"='{param}'"
                    if param != main['cur_args']['block'][-1]:
                        sql_query += ' OR'
                sql_query += " )"

        if 'priority' in main['cur_args'].keys():
            # key_val is used to convert string args to int for the database!
            key_val = {'low' : 0, 'mid' : 1, 'high' : 2}
            if main['cur_args']['priority'] != ['']:
                if (sql_query[-1] == ")"):
                    sql_query += " AND"
                sql_query += " ("
                for param in main['cur_args']['priority']:
                    sql_query += f" report.\"priorityOfIssue\"='{key_val[param]}'"
                    if param != main['cur_args']['priority'][-1]:
                        sql_query += ' OR'
                sql_query += " )"
        
        print(f"sql_query | {sql_query}")
        filtered_data = report.query.from_statement(db.text(sql_query))

        report_ids = [item.id for item in filtered_data.all()]
        main['pages'] = report.query.filter(report.id.in_(
            tuple(report_ids))).paginate(page=page, per_page=8)

        return main

    if request.method == 'GET':
        items_get = get_all_issues()

        return render_template("view_issues.html",
                               pages=items_get['pages'],
                               args=get_args_href(gbl['cur_args']))

    if request.method == 'POST':
        data = request.json

        items_post = get_all_issues()

        combine_args = {**gbl['cur_args'], **data}
        print(f"combine_args  | {combine_args}")

        items_post = get_all_issues(combine_args)

        print(get_args_href(combine_args))

        to_url = append_args(request.full_path, get_args_href(combine_args))
        print(f"to_url | {to_url}")

        # for when all param are removed
        if to_url[-1] == "?":
            to_url = './issues_table'

        return jsonify({
            'status': 'success',
            'data': {
                'items':
                render_template('issue_card.html',pages=items_post['pages'],args=get_args_href(combine_args)),
                'redirect': to_url
            }
        })

# admin page route
"""You can add the admin page route here"""

# Report page route
"""Add report page route info here"""
@app.route("/view", methods=["POST","GET"])
def view():
    if request.method == "POST":
        data = request.get_json()
        rep = report.query.get(data['id'])

        # print(f"data from POST | {data}")

        if data['item_type'] == "priority":
            if data['value'] == "Low":
                rep.priorityOfIssue = 0
            elif data['value'] == "Mid":
                rep.priorityOfIssue = 1
            elif data['value'] == "High":
                rep.priorityOfIssue = 2 
            db.session.commit()

        if data['item_type'] == "status":
            rep.issueStatus = data['value']
            db.session.commit()

        return jsonify({'status': 'success','data':{}})
        
    if request.method == "GET":
        report_id= request.args.get("id")
        rep = report.query.get(report_id)
        rep_image = rep.report_image

        if rep_image:
            image_data = base64.b64encode(rep_image[0].issue_image).decode('utf-8')
            return render_template('view_details.html', report=rep, img=image_data)
        elif rep:
            return render_template('view_details.html', report=rep)
        else:
            abort(404)

@app.route("/addreport", methods=["POST","GET"])
def add_report():

    if request.method == "POST":
        form_campus = request.form.get("campus")
        form_block = request.form.get("block")
        form_reporter = request.form.get("reporter")
        form_reporter_role = request.form.get("role")
        form_description = request.form.get("description")
        form_room_number = request.form.get("room_number")
        form_report_image = request.files["report_image"]
        refNumber = "1234567"
        print(f"Campus:{form_campus}\nBlock:{form_block}\nReporter:{form_reporter}\nReporter_Role{form_reporter_role}\nRoom Number:{form_room_number}")
        data=form_report_image.read()

        #save report to database
        
        new_report = report(campus=form_campus,campusBlock=form_block,reporter=form_reporter, reporterRole=form_reporter_role, roomNumber=form_room_number, referenceNo=refNumber,description=form_description)

        # generates referenceNo
        new_report.gen_ref()
        
        #if there's an image 
        if data:
            new_image = image(issue_image=data)
            new_report.report_image.append(new_image)
            db.session.add(new_report)
            db.session.commit()
        
        #else there's no image just add the data as is
        else:
            db.session.add(new_report)
            db.session.commit()

        return render_template('report_added_sucess.html')
    else:
        return render_template("reportscreen.html")
    

@app.route("/account-confirm/<token>")
def confirmToken(token):
    try:
        # load the token and verify the signature
        data = serializer.loads(token, max_age=3600)

        # extract the user_id and email from the data
        user_id = data['user_id']
        user_info = users.query.get(user_id)
        if user_info.confirmed ==1:
            return redirect(url_for("index"))
        else:
            # do something with the data
            user_info.confirmed = True
            db.session.commit()
      
        return redirect(url_for("index"))

    except SignatureExpired:
        # the token has expired
        return 'The confirmation link has expired.'

    except BadSignature:
        # the token is invalid
        return 'The confirmation link is invalid.'

if __name__ == "__main__":
    
    app.run(host="0.0.0.0",debug=True)
 