from app import db
from geoalchemy2 import Geometry


class Cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_supplier = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    hotline = db.Column(db.String(20))
    geom = db.Column(Geometry("POINT"))
