# Generated by Django 3.0.6 on 2020-05-07 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200507_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=2000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('explanation_text', models.CharField(max_length=2000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=2000),
        ),
    ]
