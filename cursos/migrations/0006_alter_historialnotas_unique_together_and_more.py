# Generated by Django 5.1.1 on 2024-10-11 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0005_alter_historialnotas_unique_together'),
        ('estudiantes', '0008_alter_estudiante_codigo_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='historialnotas',
            unique_together={('estudiante', 'curso')},
        ),
        migrations.RemoveField(
            model_name='historialnotas',
            name='semestre',
        ),
    ]