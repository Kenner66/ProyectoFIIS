# Generated by Django 5.1.1 on 2024-10-06 02:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0002_alter_matriculacurso_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='matricula',
            name='semestre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to='matriculas.semestre'),
        ),
    ]
