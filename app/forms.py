from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class BenevoleForm(FlaskForm):
    id = StringField("Numéro d'adhérent", validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    delegation = StringField('Délégation', validators=[DataRequired()])
    volontaire = StringField(
        "Etes vous volontaire pour participer a des missions ou des projets a l'international ?", validators=[DataRequired()])

    # contact
    email = StringField('Email', validators=[DataRequired()])
    numero = StringField('Numéro de téléphone', validators=[DataRequired()])

    # langues
    maternelle = StringField('Langue maternelle', validators=[DataRequired()])
    autonome = StringField(
        'Langues(s) avec un niveau autonome', validators=[DataRequired()])
    notions = StringField(
        'Langues(s) connues avec des notions', validators=[DataRequired()])
    lu_parlé_écrit = StringField(
        'Langue(s) lu parlé écrit', validators=[DataRequired()])

    # secteurs et domaines
    secteurs = TextAreaField('Secteurs', validators=[DataRequired()])
    domaines = TextAreaField('Domaines', validators=[DataRequired()])
    fonctions = TextAreaField('Fonctions', validators=[DataRequired()])
    competences = TextAreaField('Compétences', validators=[DataRequired()])

    # volontaire
    # inter = StringField('Compétences', validators=[DataRequired()])

    # dispo
    mission_ou_projet = StringField(
        'Etes vous disponibles pour des Missions ou des Projets ou bien les deux ?', validators=[DataRequired()])
    durée = StringField('Durée maximale des déplacements',
                        validators=[DataRequired()])
    déplacements = StringField(
        'Nombre maximum de déplacements par an', validators=[DataRequired()])

    # exp inter/bénévoles
    roles = StringField('Roles', validators=[DataRequired()])
    expérience_internationale = TextAreaField(
        'Expérience Internationale', validators=[DataRequired()])
    expérience_internationale_benevole = TextAreaField(
        'Expérience Internationale comme Bénévole', validators=[DataRequired()])
    # submit
    submit = SubmitField('Enregistrer')


class UpdateBenevoleForm(FlaskForm):
    value = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Mettre à jour')


class QueryForm(FlaskForm):
    query_field = StringField('Recherche', validators=[DataRequired()])
    sliced = StringField('Numbre', validators=[DataRequired()])
    submit = SubmitField('Rechercher')


class ChampsForm(FlaskForm):
    champs = SelectMultipleField(u'Champs', choices=[(
        'francais', 'Francais'), ('compétences', 'Compétences'), ('domaines', 'Domaines')])
    recherche = StringField('Recherche', validators=[DataRequired()])
    nombre_mot_clé = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchTextForm(FlaskForm):
    search = StringField('', validators=[DataRequired()], render_kw={
                         "placeholder": "Je recherche..."})
    submit = SubmitField('Rechercher')
