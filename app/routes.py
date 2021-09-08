from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, BenevoleForm, UpdateBenevoleForm, QueryForm
from app.models import Benevole, Langues

from app.utils import *


@app.route('/index')
def index():
    user = {'username': 'Thomas'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Login requested for user {"form.username.data"}, remember_me={form.render_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)


@app.route('/')
@app.route('/benevoles')
def get_benevoles():
    benevoles = Benevole.objects()
    # print(benevoles)
    # paginated_benevoles = Benevole.objects.paginate(page=page, per_page=10)

    # return render_template('benevoles.html', title='Benevoles', benevoles=benevoles)
    return render_template('benevoles.html', title='Benevoles', benevoles=benevoles)


@app.route('/query')
def test_query():
    benevoles = Benevole.objects(nom__icontains="st")

    return render_template('query.html', title='query_test', benevoles=benevoles)


@app.route('/register_benevole', methods=['GET', 'POST'])
def register_benevole():
    benevole = BenevoleForm()
    if benevole.validate_on_submit():
        new_benevole = Benevole()
        langues = Langues()
        langues.francais = request.form['francais']
        langues.anglais = request.form['anglais']
        langues.espagnol = request.form['espagnol']
        langues.allemand = request.form['allemand']
        langues.italien = request.form['italien']
        langues.portugais = request.form['portugais']
        langues.chinois = request.form['chinois']
        langues.russe = request.form['russe']
        langues.arabe = request.form['arabe']
        langues.autres = request.form['autres']
        new_benevole.id = int(request.form['id'])
        new_benevole.nom = request.form['nom']
        # print(type(request.form['nom']))
        new_benevole.prenom = request.form['prenom']
        new_benevole.email = request.form['email']
        new_benevole.langues = langues

        new_benevole.save()
        flash('Succès ! Nouveau bénévole bien enregistré !')
        return redirect(url_for('get_benevoles'))

    return render_template('register_benevole.html', title='register_benevole', benevole=benevole)


@app.route('/update_benevole', methods=['GET', 'POST'])
def update_benevole():
    update = UpdateBenevoleForm()
    if update.validate_on_submit():
        field = request.form['field']
        value = request.form['value']
        benevole_id = int(request.form['id'])
        # field_appartenance = appartenance(field)
        update_dict = {
            f'set__{field}': f'{value}'
        }
        Benevole.objects(id=benevole_id).update_one(
            **update_dict)
        flash(
            f"{Benevole.objects(id=benevole_id)} a bien été mise à jour!")
        return redirect(url_for('get_benevoles'))

    return render_template('update_benevole.html', title='Update_bénévole', update=update)


@app.route('/recherche', methods=['GET', 'POST'])
def query():
    query = QueryForm()
    if query.validate_on_submit():
        recherche = request.form['query_field']
        conv_recherche = convert_str_to_dict(recherche)
        dict_recherche = creation_dict(conv_recherche)
        benevoles = Benevole.objects(**dict_recherche)
        # benevoles = Benevole.objects(nom__icontains="st")
        return render_template('recherche.html', title='Recherche', recherche=recherche, benevoles=benevoles)

    return render_template('recherche_form.html', title='Recherche', query=query)
