from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/cms'
app.config['SECRET_KEY'] = 'super secret key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


from cms.Routes.admin import admin
from cms.Routes.student import student
from cms.Routes.teacher import teacher

app.register_blueprint(admin)
app.register_blueprint(student)
app.register_blueprint(teacher)