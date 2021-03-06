# Generated by Django 3.1.1 on 2020-09-08 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_customer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='is_restaurant',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='RestaurantInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('phone_num', models.CharField(max_length=35)),
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
