# Generated by Django 5.1.1 on 2024-10-10 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0008_alter_horario_unique_together_remove_horario_curso'),
        ('profesores', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horario',
            options={'verbose_name_plural': 'Horarios'},
        ),
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together={('profesor', 'seccion', 'dia_semana', 'hora_inicio', 'hora_fin')},
        ),
    ]