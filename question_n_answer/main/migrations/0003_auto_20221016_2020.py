# Generated by Django 3.2.16 on 2022-10-16 14:50

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_questionsection'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', tinymce.models.HTMLField()),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
        migrations.AddField(
            model_name='questionsection',
            name='answer',
            field=models.ManyToManyField(to='main.AnswerSection'),
        ),
    ]
