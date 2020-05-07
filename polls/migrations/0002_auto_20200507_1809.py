# Generated by Django 3.0.6 on 2020-05-07 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='questiion_type',
            field=models.CharField(choices=[('T1', 'For all students'), ('T2', 'For students not creating a question')], default='T1', max_length=2),
        ),
    ]
