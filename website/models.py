from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Product(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(150))
    orderItems = db.relationship('OrderItem', backref="product")


class Order(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    orderItem = db.relationship('OrderItem', backref='order')
    totalPrice = db.Column(db.Integer)


class OrderItem(db.Model):
    orderItemID = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'))
    qty = db.Column(db.Integer)
    # foreign key to Order
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'))


class Customer(db.Model):
    customerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(200))
    contactNum = db.Column(db.String(10))
    email = db.Column(db.String(150))
