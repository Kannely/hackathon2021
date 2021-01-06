from django.db import models


# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)


class Kibble(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    lunch_date = models.DateTimeField('Lunch date')
    weight = models.DecimalField(max_digits=10, decimal_places=2)


