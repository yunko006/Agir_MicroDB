from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, BenevoleForm, UpdateBenevoleForm, QueryForm, ChampsForm
from app.models import *

from app.utils import *
import json

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
        contact = Contact()
        experience_inter_benevole = ExperienceInterBenevole()
        domaines_et_secteurs = DomainesEtSecteurs()
        domaines_et_secteurs.secteurs = request.form['secteurs']
        domaines_et_secteurs.domaines = request.form['domaines']
        domaines_et_secteurs.fonctions = request.form['fonctions']
        domaines_et_secteurs.compétences = request.form['competences']
        contact.numéro = request.form['numero']
        contact.email = request.form['email']
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


@app.route('/recherche', methods=['GET', 'POST'])
def query():
    query = QueryForm()
    if query.validate_on_submit():
        recherche = request.form['query_field']
        # faire attention a ce que n soit bien un int
        n = int(request.form['sliced'])

        benevoles = query_function(recherche, n)
        print(benevoles)

        return render_template('recherche.html', title='Recherche', benevoles=benevoles)

    return render_template('recherche_form.html', title='Recherche', query=query)


@app.route('/help')
def help():
    return render_template('help.html', title='Aide/FAQ')


@app.route('/drop_down', methods=['GET', 'POST'])
def drop_down():
    #form = ChampsForm()
    # test = form.champs.choices
    # print(test)
    # if form.validate_on_submit():

    #     for arg in request.form:
    #         print(arg, request.form.getlist(arg))
    #     choice = request.form['champs']
    #     # query = request.form['recherche']
    #     # n = int(request.form['nombre_mot_clé'])
    #     # print(choice)
    #     if choice == 'francais':
    #         print('fr')
    #         # combinaison = f"{choice}:{query}"
    #         # converted = convert_str_to_dict(combinaison, n)
    #         # print(converted)
    #         # dicted = creation_dict(converted)

    #         # print(dicted)

    #         # benevoles = Benevole.objects(**dicted)

    #         # for b in benevoles:
    #         #     print(b.nom)
    #     else:
    #         print('autre')

    # for arg in request.form:
    #     print(arg, request.form.getlist(arg))

    #     # return redirect(url_for('drop_down'))

    # xd = request.form.copy()
    # print(xd)

    if request.method == "POST":
        recherche = request.form['recherche']
        print(recherche)
        champs = request.form['champs']
        print(champs)

        for arg in request.form:
            print(arg, request.form.getlist(arg))

        print(request.form.getlist('recherche'))

        return render_template('dropdown.html', title='Drop')
    else:
        return render_template('dropdown.html', title='DropDown')


@app.route('/recherche8', methods=['GET', 'POST'])
def recherche8():
    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list= request.form.getlist('champs')

        recherche = [string for string in recherche_list if string]
        champs = champs_list[:len(recherche)]
        print(recherche)
        print(champs)
        # zip peut entrainer un bug si deux champs sont egaux !!!! normalement aucun champs égaux
        resultat_dict = dict(zip(champs, recherche))
        print(resultat_dict)
        query = str(resultat_dict)
        for ch in ['{', '}', "'"]:
            if ch in query:
                query = query.replace(ch, '')

        print(query)
        benevoles = query_function(query, 1)
        print(benevoles)
        return render_template('recherche.html', title='Recherche', benevoles=benevoles)

    else:
        return render_template('query8.html', title='Huit')


@app.route('/bénévole/<id>')
def benevole(id):
    benevole = Benevole.objects(id=id)
    # for b in benevole:
    #     print(b.nom)
    return render_template('benevole_by_id.html', benevole=benevole)
