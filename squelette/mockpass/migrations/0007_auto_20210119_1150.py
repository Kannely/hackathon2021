# Generated by Django 3.1.5 on 2021-01-19 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mockpass', '0006_merge_20210119_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='tafA2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tafA2', to='mockpass.taf'),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='tafA3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tafA3', to='mockpass.taf'),
        ),
    ]