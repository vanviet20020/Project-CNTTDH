from app import db


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    img_price_ticket = db.Column(db.String, nullable=False)
