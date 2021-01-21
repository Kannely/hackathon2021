from django.db import models


# Create your models here.
class Obligations(models.Model):
    choices_f = [("FISE", "FISE")]
    formation = models.CharField(max_length=4, choices=choices_f)
    stage = models.IntegerField()
    ects = models.IntegerField()
    c2io = models.IntegerField()
    comp_nv3 = models.IntegerField()
    etranger = models.IntegerField()
    ielts = models.DecimalField(max_digits=3, decimal_places=1)
    choices_lv = [("A1", "A1"),
                  ("A2", "A2"),
                  ("B1", "B1"),
                  ("B2", "B2"),
                  ("C1", "C1"),
                  ("C2", "C2")]
    lv1 = models.CharField(max_length=2, choices=choices_lv)
    lv2 = models.CharField(max_length=2, choices=choices_lv)
