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
