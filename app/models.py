from app import db
import datetime


class Benevole(db.Document):
    nom = db.StringField()
    prenom = db.StringField()
    email = db.StringField()
