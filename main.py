from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

# database config
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="bgoscsfb",
    dbpass="xOIQsgnH2fM5hLsfmVLT_UZbrdlPkD78",
    dbhost="isilo.db.elephantsql.com",
    dbname="bgoscsfb")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisismyverysecretkey"
db.init_app(app)


# HomePage route
@app.route("/")
def index():

    return "This is the first page"


# This shows the login page for now. No login functionality has been added
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_query = users.query.filter_by(email=email).first()

        print(f"email:{email}\npassword{password}")

        # Check if user exists
        if user_query:
            # if user exists check if password matches password in database
            if user_query.password == password:
                return redirect(url_for('admin'))

            # if password is incorrect then give error to user that password is incorrect
            else:
                flash('Incorrect password')

            print(user_query)

        else:
            flash('Error user does not exist')

    return render_template("login.html")


@app.route("/admin")
def admin():
    return "You have succesfully been logged in"


# The function below is a test of adding a user to the database table
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
        
        return render_template('view_details.html', report=rep)


# The function below is a test of gettinng all users from database table
@app.route("/get_users")
def get_users():
    all_users = users.query.all()
    for user in all_users:
        listUser.append(user.email)
        print(user)

    return f"These are users in the system {listUser}"


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
                    sql_query += f" referenceNo LIKE '{param}%'"
                sql_query += " )"

        if 'campus' in main['cur_args'].keys():
            if main['cur_args']['campus'] != ['']:
                if (sql_query[-1] == ")"):
                    sql_query += " AND"
                sql_query += " ("
                for param in main['cur_args']['campus']:
                    sql_query += f" campus='{param}'"
                    if param != main['cur_args']['campus'][-1]:
                        sql_query += ' OR'
                sql_query += " )"

        if 'block' in main['cur_args'].keys():
            if main['cur_args']['block'] != ['']:
                if (sql_query[-1] == ")"):
                    sql_query += " AND"
                sql_query += " ("
                for param in main['cur_args']['block']:
                    sql_query += f" campusBlock='{param}'"
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
                    sql_query += f" priorityOfIssue='{key_val[param]}'"
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

@app.route("/run_models")
def run_models():
    with app.app_context():
        db.create_all()

    return "Done!"

# for testing purposes - until report screen works
@app.route('/init_report')
def init_report():

    def gen_ref():
        chs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        nm = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        ref = ''
        while len(ref)<10:
                if len(ref)<=5:
                    ref+=chs[randint(0,len(chs)-1)]
                else:
                    ref+=chs[randint(0,len(nm)-1)]
        return ref

    camp = ["Steve Biko","Ritson","ML Sultan"];
    # 0 - Low, 1 - Mid, 2 - High
    pr = [0,1,2]
    bl = ["A Block", "B Block", "C Block"]
    stat = ["Pending","In Progress","Completed"]
    rol = ["Student","Security Guard","Staff","General Worker"]
    dep = ["Information Technology","Human Resources","Finance","Logistics","Marketing"]
    p = ["Alice","John","Tom","Angelica","Timothy","Linus","Franklin"]
    def rm():
        c = ["AM","DB","BC"]
        res = c[randint(0,len(c)-1)] + str(randint(1000,3000))
        return res

    for i in range(1,48):
        new_rep = report(referenceNo=gen_ref(),campus=camp[randint(0,len(camp)-1)],
                     campusBlock=bl[randint(0,len(bl)-1)],
                     department=dep[randint(0,len(dep)-1)],
                     roomNumber=rm(),
                     reporter=p[randint(0,len(p)-1)],
                     dateReported=datetime.now(),
                     issueStatus=stat[randint(0,len(stat)-1)],
                     reporterRole=rol[randint(0,len(rol)-1)],
                     priorityOfIssue=pr[randint(0,len(pr)-1)])
        db.session.add(new_rep)
    db.session.commit()

    return "Done!"

# admin page route
"""You can add the admin page route here"""

# Report page route
"""Add report page route info here"""

if __name__ == "__main__":

    app.run(debug=True)
