from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='../templates')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../sql/company.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0034@localhost/mcompany'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mcompany'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from views import routes