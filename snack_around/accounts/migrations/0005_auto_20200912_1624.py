# Generated by Django 3.1.1 on 2020-09-12 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_restaurantimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantimage',
            old_name='property',
            new_name='info',
        ),
    ]
