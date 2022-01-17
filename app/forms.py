from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class BenevoleForm(FlaskForm):
    id = StringField("Numéro d'adhérent", validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
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
    secteurs = StringField('Secteurs', validators=[DataRequired()])
    domaines = StringField('Domaines', validators=[DataRequired()])
    fonctions = StringField('Fonctions', validators=[DataRequired()])
    competences = StringField('Compétences', validators=[DataRequired()])
    # exp inter/bénévoles
    roles = StringField('Roles', validators=[DataRequired()])
    expérience_internationale = StringField(
        'Expérience Internationale', validators=[DataRequired()])
    expérience_internationale_benevole = StringField(
        'Expérience Internationale comme Bénévole', validators=[DataRequired()])
    # submit
    submit = SubmitField('Enregistrer')


class UpdateBenevoleForm(FlaskForm):
    id = StringField("Numéro d'adhérent", validators=[DataRequired()])
    field = StringField('Champs', validators=[DataRequired()])
    value = StringField('Valeur', validators=[DataRequired()])
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
    search = StringField('Recherche', validators=[DataRequired()])
    submit = SubmitField('Rechercher')
