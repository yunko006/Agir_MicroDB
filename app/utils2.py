import itertools
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


def combinaison(l:list):
    l2 = []
    for L in range(1, len(l)+1):
        for subset in itertools.combinations(l, L):
            if subset[0] == l[0]:
                l2.append(subset)

    return l2


def convert_str_to_dict(string):
    convertedDict = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                      for element in string.split(', ')))

    return convertedDict


def tuple_to_str(tup:tuple) ->str:
    a = ', '.join(tup)
    return a


def creation_dict(test_dict: dict):
    benevole = {}

    appart = appartenance(test_dict)
    # print(appart)
    # create a loop a travers le dictionnaire
    for i, n in enumerate(test_dict):
        # permet d'assigner la valeur des keys a mot clé afin d'executer la query

        # append chaque valeur dans le dict benevole
        benevole[f"{appart[i]}__{list(test_dict.keys())[i]}__icontains"] = f"{test_dict[n]}"

    return benevole

def recherche(query:str):
    query_into_list = ['francais:maternelle', 'compétences:création', 'fonctions:enseigant']
    combinaison = combinaison(query_into_list)
    final_dict = {}
    # print(combinaison)

    for i in range(0, len(combinaison) +1):

        benevoles = Benevole.objects(combinaison[i])

        if benevoles.count() != 0:
            final_dict[combinaison[i]] = [benevole.nom for benevole in benevoles]

        else:
            final_dict[combinaison[i]] = ['Pas de bénévoles associés à cette recherche.']

    return final_dict


def input_to_validate_data(user_input:str):
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


def query_by_element(d:dict):

    query_result = {}

    for i, subdict in enumerate(d):
        # print(subdict)
        x = " ".join(list(subdict.values()))
        benevoles = Benevole.objects(**subdict)

        if benevoles.count() != 0:
            query_result[x] = [benevole for benevole in benevoles]

        else:
            query_result[x] = ['Pas de résulat.']

    return query_result
