# Generated by Django 4.2.7 on 2023-11-28 17:14

from django.db import migrations, models
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_player_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='label',
            field=models.CharField(max_length=20, validators=[game.models.validate_cell_name]),
        ),
    ]
