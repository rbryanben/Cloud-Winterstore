# Generated by Django 3.1.7 on 2021-06-01 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0011_deletedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageSettings',
            fields=[
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='SharedApp.project')),
                ('allowUserRead', models.BooleanField(default=True)),
                ('allowUserWrite', models.BooleanField(default=True)),
                ('allowAccessControl', models.BooleanField(default=True)),
            ],
        ),
    ]