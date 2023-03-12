from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *

# testing by M Mngadi
from random import randint
# end testing


app = Flask(__name__)

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
db.init_app(app)



#HomePage route
@app.route("/")
def index():
   
    return "This is the first page"


#This shows the login page for now. No login functionality has been added
@app.route("/login", methods=["GET","POST"])
def login():
     if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_query = users.query.filter_by(email=email).first()

        print(f"email:{email}\npassword{password}")

        #Check if user exists
        if user_query:
            #if user exists check if password matches password in database
            if user_query.password==password:
                 return redirect(url_for('admin'))
                 

            #if password is incorrect then give error to user that password is incorrect
            else:
                  flash('Incorrect password')
                 

            print(user_query)
            
        else:
              flash('Error user does not exist')
        
     return render_template("login.html")

@app.route("/admin")
def admin():
     return render_template("/admin_screen/admin.html")



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
     return render_template("issues_table.html",tdata=tdata_local)


# dummy data to test that the table works, will be removed later - M Mngadi
tdata_local = [
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"},
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"},
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"},
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"},
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"},
    {"title":"material confined likewise it humanity raillery an unpacked as he.","nature_of_work":"Electical","campus":"Steve Biko","block":"S Block","priority":"medium", "link":"https://www.google.com"},
    {"title":"Kept in sent gave feel will oh it we. Has pleasure procured men laughing shutters nay.","nature_of_work":"Plumbing","campus":"Ritson","block":"D Block","priority":"high", "link":"https://www.bing.com"}
    ];

#admin page route
"""You can add the admin page route here"""

#Report page route
"""Add report page route info here"""


if __name__ == "__main__":
    
    app.run(debug=True)
 