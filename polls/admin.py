from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Student_Question, Student_Choice, Student, Student_Response

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
    extra = 0


class StudentQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'explanation_text', 'by_student']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [StudentChoiceInline]


class StudentResponseInline(admin.TabularInline):
    model = Student_Response
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Student information', {'fields': ['name', 'attempted', 'group']}),
    ]
    inlines = [StudentResponseInline]

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)

admin.site.register(Student_Question, StudentQuestionAdmin)

admin.site.register(Student_Choice)

admin.site.register(Student, StudentAdmin)

admin.site.register(Student_Response)
