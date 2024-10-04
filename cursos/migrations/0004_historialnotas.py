# Generated by Django 5.1.1 on 2024-10-03 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alter_curso_ciclo'),
        ('estudiantes', '0008_alter_estudiante_codigo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialNotas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('semestre', models.CharField(max_length=10)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_notas', to='cursos.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_notas', to='estudiantes.estudiante')),
            ],
        ),
    ]