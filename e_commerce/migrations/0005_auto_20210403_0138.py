# Generated by Django 3.1.7 on 2021-04-03 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0004_auto_20210403_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_commerce.product', unique=True),
        ),
    ]