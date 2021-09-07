from app import db


class Benevole(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField()
    prenom = db.StringField()
    email = db.StringField()

    meta = {'strict': False}
