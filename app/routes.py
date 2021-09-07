from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, BenevoleForm
from app.models import Benevole


@app.route('/')
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
        new_benevole.nom = request.form['nom']
        new_benevole.prenom = request.form['prenom']
        new_benevole.email = request.form['email']
        new_benevole.save()
        flash('Succès ! Nouveau bénévole bien enregistré !')
        return redirect(url_for('get_benevoles'))

    return render_template('register_benevole.html', title='register_benevole', benevole=benevole)
