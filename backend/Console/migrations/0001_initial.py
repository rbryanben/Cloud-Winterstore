# Generated by Django 3.2.4 on 2021-07-04 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SharedApp', '0005_alter_developerclient_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDownloadObjectStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download', models.IntegerField(default=1)),
                ('indexObject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='SharedApp.indexobject')),
            ],
        ),
        migrations.CreateModel(
            name='FileDownloadInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downloaded', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SharedApp.indexobject')),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='SharedApp.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
