from flask import render_template, flash, redirect, url_for, request, session
from app import app, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, BenevoleForm, SearchTextForm
from app.models import *
from app.role_required import *

from app.utils import *


ROWS_PER_PAGE = 10

login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(username):
    return User.objects(username=username).first()


# redirect to login is user is not authenticated
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/')
@app.route('/accueil')
@login_required
def index():

    return render_template('accueil.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                login_user(user)

                next = request.args.get('next')
                if not is_safe_url(next):
                    return flask.abort(400)

                return redirect(url_for('index'))

    return render_template('login2.html', title="Sign In", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delegation')
@login_required
def accordeon_delegation():
    # get all distinct delegation to loop throught
    delegation = Benevole.objects.distinct('delegation')
    benevoles = Benevole.objects()
    return render_template('accordeon_delegation.html', title='delegation', delegation=delegation, benevoles=benevoles)


# plus utilisé pour le moment
@app.route('/benevoles')
@login_required
def get_benevoles():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)

    # all_benevoles = Benevole.objects()
    # colors = Color.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    all_benevoles = Benevole.objects.paginate(
        page=page, per_page=ROWS_PER_PAGE)

    return render_template('benevoles.html', title='Benevoles', all_benevoles=all_benevoles)


@app.route('/register_benevole', methods=['GET', 'POST'])
@AI_required
def register_benevole():
    benevole = BenevoleForm()
    if benevole.validate_on_submit():
        new_benevole = Benevole()
        langues = Langues()
        contact = Contact()
        experience_inter_benevole = ExperienceInterBenevole()
        domaines_et_secteurs = DomainesEtSecteurs()
        dispo = Disponibilités()

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
        experience_inter_benevole.expérience_internationale = request.form[
            'expérience_internationale']
        experience_inter_benevole.expérience_internationale_benevole = request.form[
            'expérience_internationale_benevole']

        dispo.mission_ou_projet = request.form['mission_ou_projet']
        dispo.durée = request.form['durée']
        dispo.nb_déplacements = request.form['déplacements']

        new_benevole.id = int(request.form['id'])
        new_benevole.nom = request.form['nom']
        new_benevole.prenom = request.form['prenom']
        new_benevole.delegation = request.form['delegation']
        new_benevole.volontaire_string = request.form['volontaire']

        new_benevole.langues = langues
        new_benevole.contact = contact
        new_benevole.DomainesEtSecteurs = domaines_et_secteurs
        new_benevole.ExperienceInterBenevole = experience_inter_benevole
        new_benevole.disponibilités = dispo

        new_benevole.save()
        flash('Succès ! Nouveau bénévole bien enregistré !')
        return redirect(url_for('accordeon_delegation'))

    return render_template('register_benevole.html', title='register_benevole', benevole=benevole)


@app.route('/update_benevole/<int:id>/<champs>', methods=['GET', 'POST'])
@login_required
def update_benevole(id, champs):

    if request.method == 'POST':
        value = request.form.get('value')
        modal_update_benevole(id, champs, value)
        flash(f"La fiche a bien été mise à jour!")
        return redirect(url_for('benevole', id=id))


@app.route('/help')
@login_required
def help():
    return render_template('help.html', title='Aide/FAQ')


@app.route('/recherche8', methods=['GET', 'POST'])
@AI_required
def recherche8():
    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list = request.form.getlist('champs')

        if request.form.get('Inter'):
            queryset_benevoles = Benevole.objects(volontaire__inter=True)

            final_query = convertion(recherche_list, champs_list)
            # final_query = test_convertion_plus_simple(recherche_list, champs_list)
            # print(final_query)
            benevoles_query = queryset_by_element(
                final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

        if request.form.get('France'):
            queryset_benevoles = Benevole.objects(
                volontaire__france_uniquement=True)

            final_query = convertion(recherche_list, champs_list)
            benevoles_query = queryset_by_element(
                final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

    else:
        return render_template('query8.html', title='Huit')


@app.route('/bénévole/<id>')
@login_required
def benevole(id):
    benevole_par_id = Benevole.objects(id=id)

    return render_template('benevole_by_id.html', benevole_par_id=benevole_par_id)


@app.route('/result_benevole_by_id', methods=['GET', 'POST'])
@login_required
def search_benevole_by_id():
    if request.method == 'POST':

        try:
            benevole_input = int(request.form.get('id'))
            benevoles_id_ou_nom = Benevole.objects(id=benevole_input)

        except ValueError:
            benevole_input = request.form.get('id')
            benevoles_id_ou_nom = Benevole.objects(nom=benevole_input.title())

    return render_template('result_benevole_by_id.html', benevoles_id_ou_nom=benevoles_id_ou_nom)


@app.route('/search_text', methods=['GET', 'POST'])
@AI_required
def search_text():
    benevoles = Benevole.objects()
    search_form = SearchTextForm()

    if search_form.validate_on_submit():
        search = request.form['search']

        benevoles_trouver_par_text = Benevole.objects.search_text(
            search).order_by('$text_score')

        # set la variable a la session pour pouvoir y aceder dans une autre route.
        session["benevoles_a_combiner"] = benevoles_trouver_par_text

        return render_template('search_text_results.html', benevoles_trouver_par_text=benevoles_trouver_par_text, search=search, search_form=search_form)

    return render_template('search_test_form.html', title='Search Text', search_form=search_form, benevoles=benevoles)


@app.route('/text_result_combinaison', methods=['GET', 'POST'])
@AI_required
def text_result_combinaison():
    base_queryset = session.get('benevoles_a_combiner')

    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list = request.form.getlist('champs')

        if request.form.get('Inter'):
            sub_queryset_benevoles = base_queryset.filter(
                volontaire__inter=True)

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, sub_queryset_benevoles)

            return render_template('combinaison_sur_texte_resultats.html', title='Résultats combinaison', benevoles_query=benevoles_query)

        if request.form.get('France'):
            sub_queryset_benevoles = base_queryset.filter(
                volontaire__france_uniquement=True)

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, queryset_benevoles)

            return render_template('combinaison_sur_texte_resultats.html', title='Résultats combinaison', benevoles_query=benevoles_query)

    else:
        return render_template('combinaison_text.html', title='Huit')


@app.route('/not-ROLE/')
@login_required
def not_ROLE():
    return render_template('unauthorized.html', title='Pas autorisé')
