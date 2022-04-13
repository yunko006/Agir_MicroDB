from flask import render_template, flash, redirect, url_for, request, session
from app import app, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, BenevoleForm, SearchTextForm, UpdateBenevoleForm, NewUserForm
from app.models import *
from app.role_required import *

from app.utils import *


ROWS_PER_PAGE = 10


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

                if 'AI' in user.roles:
                    return redirect(url_for('search_text'))
                else:
                    return redirect(url_for('accordeon_delegation'))

    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delegation')
@AI_required
def accordeon_delegation():
    # get all distinct delegation to loop throught
    delegation = Benevole.objects.distinct('delegation')
    benevoles = Benevole.objects()

    return render_template('accordeon_delegation.html', title='delegation', delegation=delegation, benevoles=benevoles)


@app.route('/benevoles')
@login_required
def get_benevoles():
    # Set the pagination configuration
    # page = request.args.get('page', 1, type=int)

    # all_benevoles = Benevole.objects()
    # colors = Color.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    # all_benevoles = Benevole.objects.paginate(
    #     page=page, per_page=ROWS_PER_PAGE)

    all_benevoles = Benevole.objects(delegation=current_user.delegation)

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
        flash('La fiche a bien été mise à jour!', 'info')
        return redirect(url_for('benevole', id=id))


@app.route('/help')
@login_required
def help():
    return render_template('help.html', title='Aide/FAQ')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/a_propos')
@login_required
def a_propos():
    return render_template('a_propos.html', title='A Propos')


@app.route('/recherche8', methods=['GET', 'POST'])
@AI_required
def recherche8():
    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list = request.form.getlist('champs')

        # if request.form.get('Inter'):
        #     queryset_benevoles = Benevole.objects(volontaire__inter=True)

        #     final_query = convertion(recherche_list, champs_list)
        #     # final_query = test_convertion_plus_simple(recherche_list, champs_list)
        #     print(final_query)

        #     benevoles_query = queryset_by_element(
        #         final_query, queryset_benevoles)

        #     print(final_query)
        #     return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

        # if request.form.get('France'):
        #     queryset_benevoles = Benevole.objects(
        #         volontaire__france_uniquement=True)

        #     final_query = convertion(recherche_list, champs_list)
        #     benevoles_query = queryset_by_element(
        #         final_query, queryset_benevoles)

        #     return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

        if request.form.get('Etendre'):
            # get tous les bénévoles en fonction de la délégation du compte qui fait une recherche
            # délégation = current_user.delegation
            # queryset_benevoles = Benevole.objects(delegation=délégation)
            queryset_benevoles = Benevole.objects.all()

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

        else:
            # prendre tous les bénévoles qui sont listés comme volontaire international
            queryset_benevoles = Benevole.objects(volontaire__inter=True)

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, queryset_benevoles)

            return render_template('recherche.html', title='Recherche', benevoles_query=benevoles_query)

    else:
        return render_template('query8.html', title='Huit')


@app.route('/bénévole/<id>', methods=['GET', 'POST'])
@login_required
def benevole(id):

    benevole_par_id = Benevole.objects(id=id)

    return render_template('benevole_by_id.html', benevole_par_id=benevole_par_id)
    # return render_template('benevole_update_form.html', benevole_par_id=benevole_par_id, form=form)


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
    # benevoles = Benevole.objects()
    # search_form = SearchTextForm()

    if request.method == 'POST':
        search = request.form['search']
        value = request.form['inlineRadioOptions']

        if value == 'RadioNational':

            benevoles_trouver_par_text = Benevole.objects.search_text(
                search).order_by('$text_score')

            # set la variable a la session (redis) pour pouvoir y acceder dans une autre route.
            session["benevoles_a_combiner"] = benevoles_trouver_par_text

            return render_template('search_text_results.html', benevoles_trouver_par_text=benevoles_trouver_par_text, search=search)

        if value == 'RadioDelegation':

            benevoles_trouver_par_text = Benevole.objects(delegation=current_user.delegation).search_text(
                search).order_by('$text_score')

            # set la variable a la session (redis) pour pouvoir y acceder dans une autre route.
            session["benevoles_a_combiner"] = benevoles_trouver_par_text

            return render_template('search_text_results.html', benevoles_trouver_par_text=benevoles_trouver_par_text, search=search)
    return render_template('search_test_form.html', title='Search Text')


@app.route('/text_result_combinaison', methods=['GET', 'POST'])
@AI_required
def text_result_combinaison():
    # demande le queryset a redis.
    base_queryset = session.get('benevoles_a_combiner')

    if request.method == 'POST':
        recherche_list = request.form.getlist('recherche')
        champs_list = request.form.getlist('champs')

        # if request.form.get('Inter'):
        if request.form.get('Etendre'):

            sub_queryset_benevoles = base_queryset

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, sub_queryset_benevoles)

            return render_template('combinaison_sur_texte_resultats.html', title='Résultats combinaison', benevoles_query=benevoles_query)

        # if request.form.get('France'):
        else:

            sub_queryset_benevoles = base_queryset.filter(
                volontaire__inter=True)

            final_query = convertion(recherche_list, champs_list)

            benevoles_query = queryset_by_element(
                final_query, sub_queryset_benevoles)

            return render_template('combinaison_sur_texte_resultats.html', title='Résultats combinaison', benevoles_query=benevoles_query)

    else:
        return render_template('combinaison_text.html', title='Huit')


@app.route('/not-ROLE/')
@login_required
def not_ROLE():
    return render_template('unauthorized.html', title='Pas autorisé')


@app.route('/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = NewUserForm()

    if form.validate_on_submit():
        new_user = User()
        new_user.username = request.form['identifiant']
        pw = request.form['password']
        crypted = bcrypt.generate_password_hash(pw).decode('utf-8')
        new_user.password = crypted
        new_user.roles = [r for r in request.form['roles']]
        new_user.delegation = request.form['delegation']

        new_user.save()

        return redirect(url_for('index'))

    return render_template('register_user.html', title='Nouveau User', form=form)
