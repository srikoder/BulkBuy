# Generated by Django 2.2.5 on 2020-05-05 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200505_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]