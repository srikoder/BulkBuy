# Generated by Django 3.0.5 on 2020-04-22 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200422_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='No description available', max_length=500),
        ),
    ]
