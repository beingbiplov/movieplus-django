# Generated by Django 2.2.5 on 2019-10-04 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_auto_20190924_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchedfilm',
            name='film',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
