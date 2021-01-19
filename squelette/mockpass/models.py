from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TAF(models.Model):
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)


class Periode(models.Model):
    choices = [("A1S1", "A1S1"),
               ("A1S2", "A1S2"),
               ("A2S1", "A2S1"),
               ("A2S2", "A2S2"),
               ("A3S1", "A3S1"),
               ("A3S2", "A3S2")]
    code = models.CharField(max_length=4, choices=choices)


class Obligations(models.Model):
    stage = models.IntegerField()
    etranger = models.IntegerField()
    ielts = models.DecimalField(max_digits=3, decimal_places=1)
    choices = [("A1", "A1"),
               ("A2", "A2"),
               ("B1", "B1"),
               ("B2", "B2"),
               ("C1", "C1"),
               ("C2", "C2")]
    lv1 = models.CharField(max_length=2, choices=choices)
    lv2 = models.CharField(max_length=2, choices=choices)


class Formation(models.Model):
    choices = [("FISE", "FISE")]
    code = models.CharField(max_length=4, choices=choices)


class UE(models.Model):
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    responsable = models.CharField(max_length=100)
    creneau = models.CharField(max_length=1)
    ects_tentes = models.IntegerField()
    c2io = models.BooleanField()


class SuivreUE(models.Model):
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE)
    grade = models.CharField(max_length=3)
    ects_obtenus = models.IntegerField()
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    # one to many eval competence


class Competence(models.Model):
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)


class EvalCompetence(models.Model):
    niveau = models.IntegerField()
    jetons_tentes = models.IntegerField()
    jetons_valides = models.IntegerField()
    choices = [("+", "+"), ('=', '='), ('-', '-')]
    note = models.CharField(max_length=1, choices=choices)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)


class Etudiant(models.Model):
    user = models.ForeignKey(User)
    nom = models.CharField(max_length=32)
    prenom = models.CharField(max_length=32)
    campus = models.CharField(max_length=32)
    TAFA2 = models.ForeignKey(TAF, on_delete=models.CASCADE)
    TAFA3 = models.ForeignKey(TAF, on_delete=models.CASCADE)
    periode_actuelle = models.ForeignKey(Periode, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    obligations = models.ForeignKey(Obligations, on_delete=models.CASCADE)
    # suivre UE one to many
