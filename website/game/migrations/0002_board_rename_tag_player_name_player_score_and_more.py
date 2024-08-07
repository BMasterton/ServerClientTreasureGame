# Generated by Django 4.2.7 on 2023-11-07 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=1)),
                ('row', models.IntegerField(default=10)),
                ('col', models.IntegerField(default=10)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='player',
            old_name='tag',
            new_name='name',
        ),
        migrations.AddField(
            model_name='player',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='col',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='row',
            field=models.IntegerField(default=0),
        ),
    ]
