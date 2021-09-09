from app import db


class DomainesEtSecteurs(db.EmbeddedDocument):
    secteurs = db.StringField(required=True)
    domaines = db.StringField(required=True)
    fonctions = db.StringField(required=True)
    compétences = db.StringField(required=True)


class Contact(db.EmbeddedDocument):
    numéro = db.StringField(required=True)
    email = db.StringField(required=True)


class Langues(db.EmbeddedDocument):
    francais = db.StringField(required=True)
    anglais = db.StringField(required=True)
    espagnol = db.StringField(required=True)
    allemand = db.StringField(required=True)
    italien = db.StringField(required=True)
    portugais = db.StringField(required=True)
    chinois = db.StringField(required=True)
    russe = db.StringField(required=True)
    arabe = db.StringField(required=True)
    autres = db.StringField(default=None)


class Benevole(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField()
    prenom = db.StringField()
    contact = db.EmbeddedDocumentField(Contact)
    langues = db.EmbeddedDocumentField(Langues)
    DomainesEtSecteurs = db.EmbeddedDocumentField(DomainesEtSecteurs)

    meta = {'strict': False}
