# Generated by Django 3.0.6 on 2020-05-23 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200522_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='consent_create_mcq',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='consent_survey',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(choices=[('G1', 'Control group'), ('G2', 'Experimental group without choice'), ('G3', 'Experimental group with choice'), ('G4', 'Group 3 choosing not to create MCQ'), ('G5', 'Group 3 choosing to create MCQ')], default='G3', max_length=2),
        ),
        migrations.CreateModel(
            name='Student_Survey_Additional_Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Student')),
            ],
        ),
    ]