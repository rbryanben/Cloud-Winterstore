# Generated by Django 3.2.4 on 2021-06-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0006_remove_filedownloadinstance_stat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedownloadobjectstat',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]