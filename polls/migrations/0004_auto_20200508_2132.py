# Generated by Django 3.0.6 on 2020-05-09 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_student_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='group',
        ),
        migrations.AddField(
            model_name='student',
            name='allotted_group',
            field=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice')], default='G3', editable=False, max_length=2),
        ),
        migrations.AddField(
            model_name='student',
            name='final_group',
            field=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice')], default=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice')], default='G3', editable=False, max_length=2), max_length=2),
        ),
    ]