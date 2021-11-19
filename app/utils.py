import itertools
from app.models import Benevole


def appartenance(champs: dict):
    appart = []

    DomainesEtSecteurs = ["secteurs", "domaines", "fonctions", "compétences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["maternelle", "autonome", "notions", "lu_parlé_écrit"]
    ExperienceInterBenevole = ["roles", "expérience_internationale", "expérience_internationale_benevole"]
    for champ in champs.keys():

        if champ in DomainesEtSecteurs:
            appart.append("DomainesEtSecteurs")

        elif champ in dispo:
            appart.append("dispo")

        elif champ in langues:
            appart.append("langues")

        elif champ in ExperienceInterBenevole:
            appart.append("ExperienceInterBenevole")

    return appart


def single_appartenance(champs: str):
    inter = ["volontaire", 'hésitation']
    DomainesEtSecteurs = ["secteurs", "domaines", "fonctions", "compétences"]
    dispo = ["missions", "projets", "duree_en_mois", "nb_deplacements_par_an"]
    langues = ["maternelle", "autonome", "notions", "lu_parlé_écrit"]
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


def creation_dict(test_dict: dict):
    benevole = {}
    # permet d'assigner la valeur des keys a mot clé afin d'executer la query
    appart = appartenance(test_dict)
    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # append chaque valeur dans le dict benevole
        benevole[f"{appart[i]}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole


def clean_data(query:str):

    for ch in ['{', '}', "'", "(", ")"]:
            if ch in query:
                query = query.replace(ch, '')

    return query


def combinaison(l:list) -> list:
    combination_list = []
    for L in range(1, len(l)+1):
        for subset in itertools.combinations(l, L):
            if subset[0] == l[0]:
                combination_list.append(subset)

    return combination_list


def convert_str_to_dict(string):
    convertedDict = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                      for element in string.split(', ')))

    return convertedDict


def tuple_to_str(tup:tuple) ->str:
    a = ', '.join(tup)
    return a


def creation_dict(test_dict: dict) -> dict:
    benevole = {}

    appart = appartenance(test_dict)
    # print(appart)
    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # permet d'assigner la valeur des keys a mot clé afin d'executer la query

        # append chaque valeur dans le dict benevole
        benevole[f"{appart[i]}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole


def input_to_validate_data(user_input:str) -> list:
    research_list = []

    user_input_as_list = user_input.split(',')
    # print(user_input_as_list)
    combinations = combinaison(user_input_as_list)

    for tup in combinations:
        clean_str = tuple_to_str(tup)
        dict_convert = convert_str_to_dict(clean_str)
        dict_to_append = creation_dict(dict_convert)

        research_list.append(dict_to_append)

    return research_list


def queryset_by_element(d:dict, query_set) -> dict:
    """
    Take a QuerySet, for each subdict in d append them to a new dict and match a benevole object

    Parameters
    ...
    d: dict
        the dict with every combination in it
    query_set : QuerySet
        The QuerySet from the mongodb

    Returns
    ...
    dict
        a new dict
    """

    query_result = {}

    for i, subdict in enumerate(d):
        # print(subdict)
        x = " ".join(list(subdict.values()))
        benevoles = query_set(**subdict)

        if benevoles.count() != 0:
            query_result[x] = [benevole for benevole in benevoles]

        else:
            query_result[x] = ['Pas de résulat.']

    return query_result


def convertion(recherche_list, champs_list):
    """
    Convert data from the form to data which can be used in the main function: queryset_by_element
    """
    # recherche and champs fields without blank one
    recherche = [string for string in recherche_list if string]
    champs = champs_list[:len(recherche)]

    # zip peut entrainer un bug si deux champs sont egaux !!!! normalement aucun champs égaux
    resultat_dict = dict(zip(champs, recherche))
    query = str(resultat_dict)
    clean_query = clean_data(query)

    # Two mains functions to run the query :
    final = input_to_validate_data(clean_query)

    return final
