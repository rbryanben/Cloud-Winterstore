# Generated by Django 3.2.4 on 2021-06-29 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedownloadinstance',
            name='stat',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='Console.filedownloadobjectstat'),
        ),
    ]