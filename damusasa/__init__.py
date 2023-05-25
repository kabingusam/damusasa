from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sam:ksam8657@localhost/damu'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


