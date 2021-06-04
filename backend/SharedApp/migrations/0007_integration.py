# Generated by Django 3.1.7 on 2021-06-01 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApp', '0006_platform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=25)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('integrationKey', models.CharField(max_length=64)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SharedApp.platform')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SharedApp.project')),
            ],
        ),
    ]