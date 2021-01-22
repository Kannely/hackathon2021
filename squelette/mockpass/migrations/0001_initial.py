# Generated by Django 3.1.5 on 2021-01-19 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('FISE', 'FISE')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Obligations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField()),
                ('etranger', models.IntegerField()),
                ('ielts', models.DecimalField(decimal_places=1, max_digits=3)),
                ('lv1', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2)),
                ('lv2', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Periode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('A1S1', 'A1S1'), ('A1S2', 'A1S2'), ('A2S1', 'A2S1'), ('A2S2', 'A2S2'), ('A3S1', 'A3S1'), ('A3S2', 'A3S2')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='TAF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('responsable', models.CharField(max_length=100)),
                ('creneau', models.CharField(max_length=1)),
                ('ects_tentes', models.IntegerField()),
                ('c2io', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SuivreUE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=3)),
                ('ects_obtenus', models.IntegerField()),
                ('periode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.periode')),
                ('ue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.ue')),
            ],
        ),
        migrations.CreateModel(
            name='EvalCompetence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.IntegerField()),
                ('jetons_tentes', models.IntegerField()),
                ('jetons_valides', models.IntegerField()),
                ('note', models.CharField(choices=[('+', '+'), ('=', '='), ('-', '-')], max_length=1)),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.competence')),
                ('ue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.suivreue')),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=32)),
                ('prenom', models.CharField(max_length=32)),
                ('campus', models.CharField(max_length=32)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.formation')),
                ('obligations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.obligations')),
                ('periode_actuelle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockpass.periode')),
                ('tafA2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tafA2', to='mockpass.taf')),
                ('tafA3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tafA3', to='mockpass.taf')),
                ('ues', models.ManyToManyField(to='mockpass.SuivreUE')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
