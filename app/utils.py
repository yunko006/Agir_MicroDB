from app.models import Benevole


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


def recursion_negative(query: str, n: int) -> dict:

    final_dict = {}
    convert_str = convert_str_to_dict(query, n)
    query_dict = creation_dict(convert_str)

    # print(benevoles.count())

    # permet de break la recursion :
    if n != 0:

        benevoles = Benevole.objects(**query_dict)

        # TODO
        if benevoles.count() != 0:
            # print(
            #     f"Bénévoles associés à la recherche: {query_dict.keys()}")
            # {recherche(query_dict): benevole.nom1, benevole.nom2, etc}
            final_dict[f"{query_dict.values()}"] = [
                benevole.nom for benevole in benevoles]

            n -= 1

            return final_dict, recursion_negative(query, n)

        else:
            # print(
            #     f"Pas de bénévoles associés à la recherche: {query_dict.keys()}")
            # {recherche(query_dict): Pas de bénévole associé}
            final_dict[f"{query_dict.values()}"] = "Pas de bénévoles associés à la recherche"

            n -= 1
            return final_dict, recursion_negative(query, n)

    else:
        return 'La recherche est arrivée à sont terme.'
