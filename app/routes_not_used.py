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


@app.route('/query')
def test_query():
    benevoles = Benevole.objects(nom__icontains="st")

    return render_template('query.html', title='query_test', benevoles=benevoles)


# not safe to use !
# @app.route('/force_update')
# @admin_required
# def update_db_from_script():

#     xd = update_benevole_with_volontaire_fied()
#     # test = create_user()

#     return xd


search text butoon:
<div class = "text-center" >
    <a type = "button" class = "btn btn-outline-primary me-2" href = "{{ url_for('text_result_combinaison') }}" > Faire une recherche par combinaison sur ces resultats < /a >
< / div >
