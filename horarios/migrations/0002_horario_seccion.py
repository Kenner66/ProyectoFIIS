# Generated by Django 5.1.1 on 2024-10-04 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='seccion',
            field=models.CharField(default=2, max_length=10),
            preserve_default=False,
        ),
    ]