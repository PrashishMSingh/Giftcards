# Generated by Django 2.2.1 on 2019-07-07 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GiftCardsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='pinCode',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
