# Generated by Django 3.2.16 on 2022-10-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20221016_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersection',
            name='answer',
            field=models.CharField(max_length=200),
        ),
    ]
