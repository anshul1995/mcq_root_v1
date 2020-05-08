import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Base_Question(models.Model):
    question_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        abstract = True


class Base_Choice(models.Model):
    choice_text = models.CharField(max_length=2000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

    class Meta:
        abstract = True


######## INSTRUCTOR QUESTIONS ########


class Question(Base_Question):
    TYPE1 = 'T1'
    TYPE2 = 'T2'
    QUESTION_TYPE_CHOICES = [
        (TYPE1, 'For all students'),
        (TYPE2, 'For students not creating a question'),
    ]
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=TYPE1,
    )


class Choice(Base_Choice):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)


######## STUDENT QUESTIONS ########


class Student(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    def get_group(self):
        return 1 + hash(self.name)%3


class Student_Question(Base_Question):
    explanation_text = models.CharField(max_length=2000)
    by_student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='creator_of',
        null=True,
    )


class Student_Choice(Base_Choice):
    question = models.ForeignKey(Student_Question, on_delete=models.CASCADE)
