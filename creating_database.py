from main import db,app

db.init_app(app)
db.create_all()