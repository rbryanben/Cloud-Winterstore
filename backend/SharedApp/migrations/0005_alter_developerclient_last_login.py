# Generated by Django 3.2.4 on 2021-07-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0004_developerclient_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developerclient',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
