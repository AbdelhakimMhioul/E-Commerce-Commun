# Generated by Django 3.1.7 on 2021-04-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rates',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
