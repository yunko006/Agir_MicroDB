from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class BenevoleForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    numero = StringField('Numéro de téléphone', validators=[DataRequired()])
    francais = StringField('Niveau de Francais', validators=[DataRequired()])
    anglais = StringField("Niveau d'Anglais", validators=[DataRequired()])
    espagnol = StringField("Niveau d'Espagnol", validators=[DataRequired()])
    allemand = StringField("Niveau d'Allemand", validators=[DataRequired()])
    italien = StringField("Niveau d'Italien", validators=[DataRequired()])
    portugais = StringField('Niveau de Portugais', validators=[DataRequired()])
    chinois = StringField('Niveau de Chinois', validators=[DataRequired()])
    russe = StringField('Niveau de Russe', validators=[DataRequired()])
    arabe = StringField('Niveau de Arabe', validators=[DataRequired()])
    autres = StringField('Autres', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class UpdateBenevoleForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    field = StringField('Champs', validators=[DataRequired()])
    value = StringField('Valeur', validators=[DataRequired()])
    submit = SubmitField('Mettre à jour')


class QueryForm(FlaskForm):
    query_field = StringField('Recherche', validators=[DataRequired()])
    submit = SubmitField('Rechercher')
