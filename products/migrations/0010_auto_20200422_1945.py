# Generated by Django 3.0.5 on 2020-04-22 19:45

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200422_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=products.models.user_directory_path),
        ),
    ]
