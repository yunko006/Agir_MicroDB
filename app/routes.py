from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, BenevoleForm, UpdateBenevoleForm, QueryForm, ChampsForm, SearchTextForm
from app.models import *

from app.utils import *

from app.update_db import update_benevole_with_volontaire_fied
# import json

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


@app.route('/register_benevole', methods=['GET', 'POST'])
def register_benevole():
    benevole = BenevoleForm()
    if benevole.validate_on_submit():
        new_benevole = Benevole()
        langues = Langues()
        contact = Contact()
        experience_inter_benevole = ExperienceInterBenevole()
        domaines_et_secteurs = DomainesEtSecteurs()

        domaines_et_secteurs.secteurs = request.form['secteurs']
        domaines_et_secteurs.domaines = request.form['domaines']
        domaines_et_secteurs.fonctions = request.form['fonctions']

        domaines_et_secteurs.compétences = request.form['competences']
        contact.numéro = request.form['numero']
        contact.email = request.form['email']

        langues.maternelle = request.form['maternelle']
        langues.autonome = request.form['autonome']
        langues.notions = request.form['notions']
        langues.lu_parlé_écrit = request.form['lu_parlé_écrit']

        experience_inter_benevole.roles = request.form['roles']
        experience_inter_benevole.expérience_internationale = request.form['expérience_internationale']
        experience_inter_benevole.expérience_internationale_benevole = request.form['expérience_internationale_benevole']
        new_benevole.id = int(request.form['id'])
        new_benevole.nom = request.form['nom']
        new_benevole.prenom = request.form['prenom']

        new_benevole.langues = langues
        new_benevole.contact = contact
        new_benevole.DomainesEtSecteurs = domaines_et_secteurs
        new_benevole.ExperienceInterBenevole = experience_inter_benevole

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
        field_appartenance = single_appartenance(field)
        update_dict = {
            f'set__{field_appartenance}__{field}': f'{value}'
        }
        Benevole.objects(id=benevole_id).update_one(
            **update_dict)
        flash(
            f"{Benevole.objects(id=benevole_id)} a bien été mise à jour!")
        return redirect(url_for('get_benevoles'))

    return render_template('update_benevole.html', title='Update_bénévole', update=update)


@app.route('/help')
def help():
    return render_template('help.html', title='Aide/FAQ')


@app.route('/recherche8', methods=['GET', 'POST'])
def recherche8():
    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list= request.form.getlist('champs')

        check_inter = request.form.get('Inter')
        check_france = request.form.get('France')

        if request.form.get('Inter'):
            queryset_benevoles = Benevole.objects(volontaire__inter=True)


            final_query = convertion(recherche_list, champs_list)
            benevoles = queryset_by_element(final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles=benevoles)

        if request.form.get('France'):
            queryset_benevoles = Benevole.objects(volontaire__france_uniquement=True)

            final_query = convertion(recherche_list, champs_list)
            benevoles = queryset_by_element(final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles=benevoles)

    else:
        return render_template('query8.html', title='Huit')


@app.route('/bénévole/<id>')
def benevole(id):
    benevole = Benevole.objects(id=id)

    return render_template('benevole_by_id.html', benevole=benevole)


@app.route('/search_text', methods=['GET', 'POST'])
def search_text():
    search_form = SearchTextForm()

    if search_form.validate_on_submit() and request.method == 'POST':
        search = request.form['search']

        benevoles = Benevole.objects.search_text(search).order_by('$text_score')

        return render_template('search_text_results.html', benevoles=benevoles, search=search)

    return render_template('search_test_form.html', title='Search Text', search_form=search_form)


@app.route('/force_update')
def update_db_from_script():

    xd = update_benevole_with_volontaire_fied()

    return xd
