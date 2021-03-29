# Generated by Django 3.1.7 on 2021-03-29 09:26

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('photo', models.ImageField(upload_to='')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='e_commerce.person')),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('nbElementProd', models.PositiveBigIntegerField()),
                ('resteProd', models.PositiveBigIntegerField()),
                ('profitProd', models.FloatField()),
            ],
            bases=('e_commerce.person',),
        ),
    ]
