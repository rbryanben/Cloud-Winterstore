# Generated by Django 3.2.4 on 2021-07-11 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0009_integration_stored'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='devices',
            field=models.IntegerField(default=0),
        ),
    ]
