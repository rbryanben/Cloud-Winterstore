# Generated by Django 3.2.4 on 2021-07-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0007_teamcollaboration_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='pull',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='integration',
            name='push',
            field=models.IntegerField(default=0),
        ),
    ]