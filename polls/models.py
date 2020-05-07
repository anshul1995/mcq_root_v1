import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Base_Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        abstract = True

class Question(Base_Question):
    TYPE1 = 'T1'
    TYPE2 = 'T2'
    QUESTION_TYPE_CHOICES = [
        (TYPE1, 'For all students'),
        (TYPE2, 'For students not creating a question'),
    ]
    questiion_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=TYPE1,
    )


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
