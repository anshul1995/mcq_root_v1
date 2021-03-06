import datetime
import random

from django.db import models
from django.utils import timezone

# Create your models here.
class Base_Question(models.Model):
    question_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    def __str__(self):
        return self.question_text
    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now

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
    sort_order = models.IntegerField(default=0)


class Choice(Base_Choice):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)


class Survey_Question(Base_Question):
    TYPE1 = 'T1'
    TYPE2 = 'T2'
    TYPE3 = 'T3'
    TYPE4 = 'T4'
    QUESTION_TYPE_CHOICES = [
        (TYPE1, 'For groups 1, 2, 4 and 5'),
        (TYPE2, 'For groups 2, 4 and 5'),
        (TYPE3, 'For group 4'),
        (TYPE4, 'For group 5'),
    ]
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=TYPE1,
    )
    sort_order = models.IntegerField(default=0)


######## STUDENT QUESTIONS ########


class Student(models.Model):
    GROUP1 = 'G1'
    GROUP2 = 'G2'
    GROUP3 = 'G3'
    GROUP4 = 'G4'
    GROUP5 = 'G5'
    GROUP_TYPE_CHOICES = [
        (GROUP1, 'Control group'),
        (GROUP2, 'Experimental group without choice'),
        (GROUP3, 'Experimental group with choice'),
        (GROUP4, 'Group 3 choosing not to create MCQ'),
        (GROUP5, 'Group 3 choosing to create MCQ'),
    ]
    STAGE1 = 'S1'
    STAGE2 = 'S2'
    STAGE3 = 'S3'
    STAGE_CHOICES = [
        (STAGE1, 'Quiz'),
        (STAGE2, 'Survey'),
        (STAGE3, 'Results'),
    ]
    name = models.CharField(max_length=200, unique=True)
    stage = models.CharField(
        max_length=2,
        choices=STAGE_CHOICES,
        default='S1',
    )
    group = models.CharField(
        max_length=2,
        choices=GROUP_TYPE_CHOICES,
        default='G1',
    )
    consent_create_mcq = models.BooleanField(default=False)
    consent_survey = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Student_Question(Base_Question):
    explanation_text = models.CharField(max_length=2000)
    topics = models.CharField(max_length=1000, default="")
    by_student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='creator_of',
    )


class Student_Question_Topic(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Student_Choice(Base_Choice):
    question = models.ForeignKey(Student_Question, on_delete=models.CASCADE)


class Student_Response(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student_id) + ' : ' + str(self.question_id) + ' - ' + str(self.choice_id)


class Student_Survey_Response(models.Model):
    CHOICE1 = 'C1'
    CHOICE2 = 'C2'
    CHOICE3 = 'C3'
    CHOICE4 = 'C4'
    CHOICE5 = 'C5'
    CHOICE_TYPE_CHOICES = [
        (CHOICE1, 'Strongly disagree'),
        (CHOICE2, 'Somewhat disagree'),
        (CHOICE3, 'Neither agree nor disagree'),
        (CHOICE4, 'Somewhat agree'),
        (CHOICE5, 'Strongly agree'),
    ]
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    survey_question_id = models.ForeignKey(Survey_Question, on_delete=models.CASCADE)
    survey_choice_id = models.CharField(
        max_length=2,
        choices=CHOICE_TYPE_CHOICES,
        default='C1',
    )

    def __str__(self):
        return str(self.student_id) + ' : ' + str(self.survey_question_id) + ' - ' + str(self.survey_choice_id)


class Student_Survey_Additional_Text(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.student_id) + ' : ' + self.text

class Log(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    element_type = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    element_id = models.CharField(max_length=100)
    client_timestamp = models.CharField(max_length=100, default="")
    def __str__(self):
        return str(self.student_id) + ' : ' + str(self.action) + ' ' + str(self.element_type) + ' ' + str(self.element_id)
