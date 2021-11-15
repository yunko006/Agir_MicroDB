from app.models import Benevole, Disponibilités


def update_benevole_with_volontaire_fied():
    benevoles = Benevole.objects.all()

    for b in benevoles:
        # b.volontaire = Volontaire()
        # b.volontaire.inter = True
        # b.volontaire.france_uniquement = False
        b.disponibilités = Disponibilités()
        b.disponibilités.mission_ou_projet = "Missions individuelles; Projets en équipe"
        b.disponibilités.durée = "Moins de 15 jours"
        b.disponibilités.nb_déplacements = "4 ou plus"
        b.save()
