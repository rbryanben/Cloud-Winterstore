# Generated by Django 3.1.7 on 2021-05-22 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApplication', '0009_recoveryobject_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='recoveryobject',
            name='expiry',
            field=models.DateTimeField(default='2020-01-01 00:01:00'),
        ),
    ]