# Generated by Django 3.2.16 on 2022-10-17 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_answersection_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersection',
            name='answer',
            field=models.TextField(),
        ),
    ]
