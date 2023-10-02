from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from readability.config.key import secret_key
# from dotenv import load_dotenv
from os import getenv

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = secret_key

# Link to MySQL database hosted by Cardiff University. Insert you username and password below.
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://@csmysql.cs.cf.ac.uk:3306/c21016073_jrt'

db = SQLAlchemy(app)

from readability import routes