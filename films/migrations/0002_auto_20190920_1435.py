# Generated by Django 2.2.5 on 2019-09-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favfilm',
            name='film1',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='favfilm',
            name='film2',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='favfilm',
            name='film3',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
