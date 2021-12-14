from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'bcdae24d30fd163c00cdd40bb6d9ef22'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../sql/company.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0034@localhost/mcompany'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mcompany'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from views import routes
from rest import projects_rest