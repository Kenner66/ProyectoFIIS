# Generated by Django 5.1.1 on 2024-10-10 16:07

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0008_alter_estudiante_codigo_and_more'),
        ('matriculas', '0003_semestre_alter_matricula_semestre'),
        ('semestre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricula',
            name='semestre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='semestre.semestre'),
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='activa',
        ),
        migrations.AddField(
            model_name='matricula',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiantes.estudiante'),
        ),
        migrations.DeleteModel(
            name='MatriculaCurso',
        ),
        migrations.DeleteModel(
            name='Semestre',
        ),
    ]