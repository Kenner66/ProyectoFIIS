# Generated by Django 5.1.1 on 2024-10-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0005_matriculacurso'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='activa',
            field=models.BooleanField(default=True),
        ),
    ]
