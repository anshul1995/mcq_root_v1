# Generated by Django 3.0.6 on 2020-05-09 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_student_attempted'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice')], default='G3', max_length=2),
        ),
    ]
