# Generated by Django 5.1.1 on 2024-10-04 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0004_alter_horario_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccion',
            name='semestre',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
