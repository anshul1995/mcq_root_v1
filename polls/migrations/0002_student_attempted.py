# Generated by Django 3.0.6 on 2020-05-08 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
    ]
