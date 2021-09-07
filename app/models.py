from app import db


class Benevole(db.Document):
    nom = db.StringField()
    prenom = db.StringField()
    email = db.StringField()
