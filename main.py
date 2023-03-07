from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, users,account_history,notice_board,report,report_comments



app = Flask(__name__)

#database config
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="bgoscsfb",
    dbpass="xOIQsgnH2fM5hLsfmVLT_UZbrdlPkD78",
    dbhost="isilo.db.elephantsql.com",
    dbname="bgoscsfb"
)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#HomePage route
@app.route("/")
def index():
   
    return "Database working"

@app.route("/create_user")
def create_user():
        new_user = users(first_name = "Khanya", surname="DaSilva", email= "somehting@microsoft.com", password="asadsdasdasd", username = "hello from the other side", user_role="admin")
        db.session.add(new_user)
        db.session.commit()

        return "User created"

listUser=[]

@app.route("/get_users")
def get_users():
    all_users = users.query.all()
    for user in all_users:
          listUser.append(user.first_name)
          print(user)

    return f"These are users in the system {listUser}"

       




#admin page route
"""You can add the admin page route here"""

#Report page route
"""Add report page route info here"""


if __name__ == "__main__":
    
    app.run(debug=True)
 