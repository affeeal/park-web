# Generated by Django 4.2 on 2023-06-20 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='AnswerCorrect',
        ),
    ]