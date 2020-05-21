from django.contrib import admin

# Register your models here.

from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ('votes',)
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'question_type']}),
        ('Date information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    readonly_fields = ('pub_date',)
    inlines = [ChoiceInline]


class SurveyQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'question_type']}),
        ('Date information', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
    ]
    readonly_fields = ('pub_date',)


class StudentChoiceInline(admin.TabularInline):
    model = Student_Choice
    readonly_fields = ('question', 'choice_text', 'is_correct',)
    can_delete = False
    extra = 0


class StudentQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'explanation_text', 'by_student']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    readonly_fields = ('pub_date', 'question_text',
                       'explanation_text', 'by_student',)
    inlines = [StudentChoiceInline]


class StudentResponseInline(admin.TabularInline):
    model = Student_Response
    readonly_fields = ('student_id','question_id','choice_id',)
    can_delete = False
    extra = 0


class StudentSurveyResponseInline(admin.TabularInline):
    model = Student_Survey_Response
    readonly_fields = ('student_id', 'survey_question_id', 'survey_choice_id',)
    can_delete = False
    extra = 0

class StudentQuestionResponseInline(admin.TabularInline):
    model = Student_Question
    readonly_fields = ('question_text', 'explanation_text',)
    can_delete = False
    extra = 0


class StudentLogInline(admin.TabularInline):
    model = Log
    readonly_fields = ('student_id', 'time', 'element_type', 'action','element_id',)
    can_delete = False
    extra = 0


class LogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': [
         'student_id', 'time', 'element_type', 'action', 'element_id']}),
    ]
    readonly_fields = ('student_id', 'time', 'element_type',
                       'action', 'element_id',)


class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Student information', {'fields': ['name', 'stage', 'group', 'id']}),
    )
    readonly_fields = ('id','name','stage',)
    inlines = [StudentResponseInline,
               StudentQuestionResponseInline,
               StudentSurveyResponseInline,
               StudentLogInline]

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)

admin.site.register(Survey_Question, SurveyQuestionAdmin)

admin.site.register(Student_Question, StudentQuestionAdmin)

admin.site.register(Student_Choice)

admin.site.register(Student, StudentAdmin)

admin.site.register(Student_Response)

admin.site.register(Student_Survey_Response)

admin.site.register(Log, LogAdmin)
