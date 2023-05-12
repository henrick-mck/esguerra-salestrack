from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secure'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oimoamxvyzumdo:1381e345ff764687592faa6577ba6de5e7d8ed067127a78d9e752a6aba8bac2d@ec2-3-232-218-211.compute-1.amazonaws.com:5432/danh8u46qtvtuh'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Product, Order, OrderItem, Customer

    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
