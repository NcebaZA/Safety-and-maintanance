from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://snmuk0n4ibb90h3tn0qm:pscale_pw_PDs9RvKc4IHBtwg0Vv3AWtvKlOkkNrnRusUx5WeodsYd@maintenance/db"
app.config['SQLALCHEMY_TRACL_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():

    return "THis is the first route"




if __name__ == "__main__":
    app.run(debug=True)