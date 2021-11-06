from app.models import Benevole


def appartenance(champs: dict):
    appart = []
    inter = ["volontaire", 'hésitation']
    DomainesEtSecteurs = ["secteurs", "domaines", "fonctions", "compétences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["francais", "anglais", "allemand", "espagnol",
               "italien", "portuguais", "chinois", "russe", "arabe", "autres"]
    ExperienceInterBenevole = ["roles", "expérience_internationale", "expérience_internationale_benevole"]
    for champ in champs.keys():

        if champ in inter:
            appart.append("inter")

        elif champ in DomainesEtSecteurs:
            appart.append("DomainesEtSecteurs")

        elif champ in dispo:
            appart.append("dispo")

        elif champ in langues:
            appart.append("langues")

        elif champ in ExperienceInterBenevole:
            appart.append("ExperienceInterBenevole")

    return appart
# resultat = {
#   'langues__anglais__icontains': 'notions',
#   'langues__francais__icontains': 'maternelle
#}


def single_appartenance(champs: str):
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


def convert_str_to_dict(string: str, n: int):
    convertedDict = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                      for element in string.split(', ')[:n]))

    return convertedDict


def creation_dict(test_dict: dict):
    benevole = {}
    # permet d'assigner la valeur des keys a mot clé afin d'executer la query
    appart = appartenance(test_dict)
    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # append chaque valeur dans le dict benevole
        benevole[f"{appart[i]}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole


def query_function(query: str, n: int) ->dict:
    """
    Teste les combinaisons d'input et appends les résultats dans un dict
    """
    final_dict = {}
    lenght = (len(query.split(',')))

    convert_str = convert_str_to_dict(query, n)

    while n != (lenght + 1):

        query_dict = creation_dict(convert_str)
        x = " ".join(list(query_dict.values()))
        benevoles = Benevole.objects(**query_dict)

        if benevoles.count() != 0:

            final_dict[x] = [benevole.nom for benevole in benevoles]
            n += 1
            convert_str = convert_str_to_dict(query, n)

        else:

            final_dict[x] = "Pas dé bénévoles"

            new_query = pop_item(query, n)
            n += 1
            convert_str = convert_str_to_dict(new_query, n)

    return final_dict


def pop_item(query:str, n:int) ->str:

    query_list = query.split(',')
    query_list.pop(n - 1)
    new_query = ','.join(query_list)

    return new_query
