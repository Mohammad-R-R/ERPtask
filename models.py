from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime


db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String(50), primary_key=True)
    def __repr__(self):
        return f":{self.product_id}"

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String(50), primary_key=True)
    def __repr__(self):
        return f":{self.location_id}"


class ProductMovement(db.Model):
    __tablename__ = 'productMovement'
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f":{self.movement_id}"
