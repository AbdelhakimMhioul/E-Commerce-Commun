# Generated by Django 3.1.7 on 2021-04-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0005_auto_20210403_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rates',
            field=models.PositiveIntegerField(default=1),
        ),
    ]