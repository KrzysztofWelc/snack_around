# Generated by Django 3.1.1 on 2020-09-11 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200908_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='accounts.restaurantinfo')),
            ],
        ),
    ]
