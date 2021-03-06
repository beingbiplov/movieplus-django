# Generated by Django 2.2.5 on 2019-09-24 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0002_auto_20190920_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favfilm',
            name='film1',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='favfilm',
            name='film2',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='favfilm',
            name='film3',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.CreateModel(
            name='WatchedFilm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.CharField(blank=True, max_length=25)),
                ('date_watched', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
