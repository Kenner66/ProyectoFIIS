# Generated by Django 5.1.1 on 2024-10-17 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0008_alter_estudiante_codigo_and_more'),
        ('matriculas', '0006_matricula_activa'),
        ('semestre', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='matricula',
            unique_together={('estudiante', 'semestre')},
        ),
    ]
