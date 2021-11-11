from app.models import Benevole, Volontaire


def update_benevole_with_volontaire_fied():
    benevoles = Benevole.objects.all()

    for b in benevoles:
        b.volontaire = Volontaire()
        b.volontaire.inter = True
        b.volontaire.france_uniquement = False
        b.save()
