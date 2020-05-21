# Generated by Django 3.0.6 on 2020-05-21 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20200520_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice'), ('G4', 'Group 3 choosing not to create MCQ'), ('G5', 'Group 3 choosing to create MCQ')], default='G1', max_length=2),
        ),
    ]
