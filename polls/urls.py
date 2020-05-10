from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/info/', views.info, name='info'),
    path('<int:student_id>/quiz/', views.quiz, name='quiz'),
    path('<int:student_id>/subimt/', views.submit, name='submit'),
    path('<int:student_id>/results/', views.results, name='results'),
]
