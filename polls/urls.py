from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:student_id>/', views.quiz, name='quiz'),
    # ex: /polls/5/results/
    path('<int:student_id>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/submit/
    path('<int:student_id>/subimt/', views.submit, name='submit'),
]
