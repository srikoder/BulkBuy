# Generated by Django 3.0.2 on 2020-04-19 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='reviews',
        ),
    ]
