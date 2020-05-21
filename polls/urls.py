from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/quiz/', views.quiz, name='quiz'),
    path('<int:student_id>/quiz/quiz-log/', views.quiz_log, name='quiz_log'),
    path('<int:student_id>/quiz/G3-choice/', views.g3_choice, name='g3_choice'),
    path('<int:student_id>/subimt_quiz/', views.submit_quiz, name='submit_quiz'),
    path('<int:student_id>/survey/', views.survey, name='survey'),
    path('<int:student_id>/submit_survey/', views.submit_survey, name='submit_survey'),
    path('<int:student_id>/results/', views.results, name='results'),
]
