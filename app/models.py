from app import db, login_manager
from flask_login import UserMixin


class Disponibilités(db.EmbeddedDocument):
    mission_ou_projet = db.StringField()
    durée = db.StringField()
    nb_déplacements = db.StringField()


class Volontaire(db.EmbeddedDocument):
    inter = db.BooleanField(required=True, default=True)
    france_uniquement = db.BooleanField(default=False)


class ExperienceInterBenevole(db.EmbeddedDocument):
    roles = db.StringField(required=True)
    expérience_internationale = db.StringField()
    expérience_internationale_benevole = db.StringField()


class DomainesEtSecteurs(db.EmbeddedDocument):
    secteurs = db.StringField(required=True)
    domaines = db.StringField(required=True)
    fonctions = db.StringField(required=True)
    compétences = db.StringField(required=True)


class Contact(db.EmbeddedDocument):
    numéro = db.StringField(required=True)
    email = db.StringField(required=True)


class Langues(db.EmbeddedDocument):
    maternelle = db.StringField()
    autonome = db.StringField()
    notions = db.StringField()
    lu_parlé_écrit = db.StringField()
    ne_connait_pas = db.StringField()
    autres = db.StringField(default=None)


class Benevole(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField()
    prenom = db.StringField()
    # delegation
    delegation = db.StringField()
    contact = db.EmbeddedDocumentField(Contact)
    langues = db.EmbeddedDocumentField(Langues)
    DomainesEtSecteurs = db.EmbeddedDocumentField(DomainesEtSecteurs)
    ExperienceInterBenevole = db.EmbeddedDocumentField(ExperienceInterBenevole)
    volontaire = db.EmbeddedDocumentField(Volontaire)
    disponibilités = db.EmbeddedDocumentField(Disponibilités)

    meta = {'strict': False}


class User(db.Document, UserMixin):

    meta = {'collection': 'users', 'strict': False}
    username = db.StringField(max_length=20)
    password = db.StringField()
    authenticated = db.BooleanField(default=False)
    is_active = db.BooleanField(default=True)
    roles = db.ListField(db.StringField(), default=['AI'])

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_role(self):
        return self.roles


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     # if username not in users:
#     #     return

#     user = User()
#     user.id = username
#     return user
