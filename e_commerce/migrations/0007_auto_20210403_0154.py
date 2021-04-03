# Generated by Django 3.1.7 on 2021-04-03 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0006_auto_20210403_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rates',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]