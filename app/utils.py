def appartenance(champs: dict):
    appart = []
    inter = ["volontaire", 'hésitation']
    DomainesEtSecteurs = ["secteurs", "domaines", "fonctions", "compétences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["francais", "anglais", "allemand", "espagnol",
               "italien", "portuguais", "chinois", "russe", "arabe", "autres"]
    exp_international = ["roles", "experience_inter", "description_exp",
                         "experience_benevole", "connaissance_structure_inter"]
    for champ in champs.keys():

        if champ in inter:
            appart.append("inter")

        elif champ in DomainesEtSecteurs:
            appart.append("DomainesEtSecteurs")

        elif champ in dispo:
            appart.append("dispo")

        elif champ in langues:
            appart.append("langues")

        elif champ in exp_international:
            appart.append("exp_international")

    return appart
# resultat = {
#   'langues__anglais__icontains': 'notions',
#   'langues__francais__icontains': 'maternelle
#}


def single_appartenance(champs):
    inter = ["volontaire", 'hésitation']
    DomainesEtSecteurs = ["secteurs", "domaines", "fonctions", "compétences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["francais", "anglais", "allemand", "espagnol",
               "italien", "portuguais", "chinois", "russe", "arabe", "autres"]
    exp_international = ["roles", "experience_inter", "description_exp",
                         "experience_benevole", "connaissance_structure_inter"]
    contact = ["numéro", "email"]

    if champs in inter:
        return "inter"

    elif champs in DomainesEtSecteurs:
        return "DomainesEtSecteurs"

    elif champs in dispo:
        return "dispo"

    elif champs in langues:
        return "langues"

    elif champs in exp_international:
        return "exp_international"

    elif champs in contact:
        return "contact"

    else:
        return f"{champs}"


def convert_str_to_dict(string):
    convertedDict = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                      for element in string.split(', ')))

    return convertedDict


def creation_dict(test_dict: dict):
    benevole = {}

    appart = appartenance(test_dict)
    print(appart)
    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # permet d'assigner la valeur des keys a mot clé afin d'executer la query

        # append chaque valeur dans le dict benevole
        benevole[f"{appart[i]}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole
