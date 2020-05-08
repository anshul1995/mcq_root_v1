from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Student_Question, Student_Choice, Student

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'question_type']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


class StudentChoiceInline(admin.TabularInline):
    model = Student_Choice


class StudentQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'explanation_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [StudentChoiceInline]

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)

admin.site.register(Student_Question, StudentQuestionAdmin)

admin.site.register(Student_Choice)

admin.site.register(Student)
