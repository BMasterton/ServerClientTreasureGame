# Generated by Django 4.2.7 on 2023-11-20 19:09

from django.db import migrations, models
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_board_label_alter_player_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='col',
            field=models.IntegerField(default=10, validators=[game.models.validate_col_range]),
        ),
        migrations.AlterField(
            model_name='board',
            name='label',
            field=models.CharField(default='.', max_length=20, validators=[game.models.validate_cell_name]),
        ),
        migrations.AlterField(
            model_name='board',
            name='row',
            field=models.IntegerField(default=10, validators=[game.models.validate_row_range]),
        ),
        migrations.AlterField(
            model_name='board',
            name='value',
            field=models.IntegerField(default=0, validators=[game.models.validate_value_amount]),
        ),
        migrations.AlterField(
            model_name='player',
            name='col',
            field=models.IntegerField(default=0, validators=[game.models.validate_col_range]),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=20, validators=[game.models.validate_unique_name]),
        ),
        migrations.AlterField(
            model_name='player',
            name='row',
            field=models.IntegerField(default=0, validators=[game.models.validate_row_range]),
        ),
    ]