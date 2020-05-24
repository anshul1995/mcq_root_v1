# Generated by Django 3.0.6 on 2020-05-24 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200523_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Question_Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='student_question',
            name='topics',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
