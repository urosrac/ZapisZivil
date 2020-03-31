import os
from sqla_wrapper import SQLAlchemy
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))
class FoodItems(db.Model):
    __tablename__ = 'fooditems'
    ID = db.Column(db.Integer, primary_key=True)
    ImeZivila = db.Column(db.String, nullable=False)
    DatumVpisa = db.Column(db.DateTime, nullable=False)
    DatumPoteka = db.Column(db.DateTime, nullable=True)
    Kolicina = db.Column(db.Integer, nullable=False, index=True)
    IsExpired = db.Column(db.Boolean, nullable=False, index=True)
    IsRemoved = db.Column(db.Boolean, nullable=False, index=True)