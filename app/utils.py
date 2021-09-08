def appartenance(champs):
    inter = ["volontaire", 'hésitation']
    domaines_secteurs = ["secteurs", "domaines", "fonctions", "competences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["francais", "anglais", "allemand", "espagnol",
               "italien", "portuguais", "chinois", "russe", "arabe", "autres"]
    exp_international = ["roles", "experience_inter", "description_exp",
                         "experience_benevole", "connaissance_structure_inter"]

    if champs in inter:
        return "inter"

    elif champs in domaines_secteurs:
        return "domaines_secteurs"

    elif champs in dispo:
        return "dispo"

    elif champs in langues:
        return "langues"

    elif champs in exp_international:
        return "exp_international"

    else:
        return f"{champs}"


def convert_str_to_dict(string):
    convertedDict = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                      for element in string.split(', ')))

    return convertedDict


def creation_dict(test_dict):
    benevole = {}

    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # permet d'assigner la valeur des keys a mot clé afin d'executer la query
        for k in list(test_dict.keys()):
            appart = (appartenance(k))
        # append chaque valeur dans le dict benevole
        benevole[f"{appart}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole
