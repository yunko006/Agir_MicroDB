from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
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
    submit = SubmitField('Enregistrer')


class UpdateBenevoleForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    field = StringField('Champs', validators=[DataRequired()])
    value = StringField('Valeur', validators=[DataRequired()])
    submit = SubmitField('Mettre à jour')
