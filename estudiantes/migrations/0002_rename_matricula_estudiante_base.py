# Generated by Django 5.1.1 on 2024-09-25 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudiante',
            old_name='matricula',
            new_name='base',
        ),
    ]
