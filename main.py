from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

# testing by M Mngadi
from random import randint
from sqlalchemy.exc import IntegrityError
# end testing

app = Flask(__name__)

#database config
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="bgoscsfb",
    dbpass="xOIQsgnH2fM5hLsfmVLT_UZbrdlPkD78",
    dbhost="isilo.db.elephantsql.com",
    dbname="bgoscsfb")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisismyverysecretkey"
db.init_app(app)


#HomePage route
@app.route("/")
def index():

    return "This is the first page"


#This shows the login page for now. No login functionality has been added
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_query = users.query.filter_by(email=email).first()

        print(f"email:{email}\npassword{password}")

        #Check if user exists
        if user_query:
            #if user exists check if password matches password in database
            if user_query.password == password:
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
    return "You have succesfully been logged in"


##The function below is a test of adding a user to the database table
@app.route("/create_user")
def create_user():
    new_user = users(first_name="Nokthula",
                     surname="Makhanya",
                     email="22023482@dut4life.ac.za",
                     password="2023",
                     username="thuli012",
                     user_role="admin")
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


listUser = []


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


#This function takes user to issues table.
@app.route("/issues_table", methods=['GET', 'POST'])
def show_issues():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '', type=str)
    campus = request.args.get('campus', '', type=str)

    global l

    if request.method == 'GET':
        l = {'cur_args': request.args.to_dict() , 'pages': {}}
        print(f"Inside GET | {l['cur_args']}" )

        l['pages'] = tdataDB.query
        
        if keyword!='':
            l['pages'] = l['pages'].filter(tdataDB.title.like(f'{keyword}%'))
        elif campus!='':
            l['pages'] = l['pages'].filter_by(campus=(f'{campus}'))

        l['pages'] = l['pages'].paginate(page=page,per_page=4)

        return render_template("issues_table.html",
                               pages=l['pages'],
                               args=l['cur_args'])

    if request.method == 'POST':
        search_for = request.form['search_for']

        l = {'cur_args': request.args.to_dict() , 'pages': {}}
        print(f"Inside POST | {l['cur_args']}")

        l['pages']=tdataDB.query.filter(tdataDB.title.like(f'{search_for}%')).paginate(page=1,per_page=4)

        to_url = request.full_path
        if to_url[-1]=='?':
            to_url += f"keyword={search_for}"
            l['cur_args']['keyword']=search_for
        else:
            to_url = request.path

        return jsonify({'status' : 'success', 'data' : {'items':render_template('issue_card.html',pages=l['pages'], args=l['cur_args']), 'search_for' : search_for, 'redirect' : to_url}})


# testing
@app.route('/filter', methods=['POST'])
def filter_data():
    data = request.json
    # Filter the data based on the selected filters
    # ...
    print(f"data from json | {data}")
    l = {
        'cur_args': request.args.to_dict(),
        'pages': tdataDB.query.paginate(page=1, per_page=4)
    }

    l['pages'] = tdataDB.query.filter_by(campus=data['uCampus'][0]).paginate(
        page=1, per_page=4)

    # %2B
    to_url = request.full_path
    if to_url[-1]=='?':
        if data['uCampus'] != []:
            to_url += f"campus="
            for uitem in data['uCampus']:
                "{data['uCampus']}"
        #l['cur_args']['campus']=campus
    else:
        to_url = request.path

    response = {
        'status': 'success',
        'data': {
            'items':
            render_template('issue_card.html',
                            pages=l['pages'],
                            args=l['cur_args']),
            'redirect' : "./issues_table"
        }
    }
    return jsonify(response)


@app.route("/i_tdata")
def i_tdata():
    return "Completed!"


def add_item(idPar):
    tcamp = ["Steve Biko", "Ritson", "ML Sultan"]
    tpriority = ["low", "mid", "high"]

    new_issue = tdataDB(id=idPar,
                        title=str(idPar),
                        block=chr(randint(65, 90)) + " block",
                        campus=tcamp[randint(0, 2)],
                        priority=tpriority[randint(0, 2)])
    db.session.add(new_issue)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def remove_item(id):
    item = db.db.get_or_404(tdataDB, id)
    db.session.delete(item)
    db.session.commit()


@app.route("/get_issues")
def get_issues():

    tdata_local = []
    all_issues = tdataDB.query.all()
    for item in all_issues:
        tdata_local.append(item.title)

    return f"Issues = {tdata_local}"


#admin page route
"""You can add the admin page route here"""

#Report page route
"""Add report page route info here"""

if __name__ == "__main__":

    app.run(debug=True)
