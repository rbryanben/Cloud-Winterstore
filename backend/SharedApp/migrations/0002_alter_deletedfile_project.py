# Generated by Django 3.2.4 on 2021-06-19 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedfile',
            name='project',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='SharedApp.project'),
        ),
    ]