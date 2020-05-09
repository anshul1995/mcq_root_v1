from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from .models import Question, Choice, Student, Student_Choice, Student_Question, Student_Response
from .forms import LoginForm 


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        f = LoginForm()
    else:
        f = LoginForm(request.POST)
        if f.is_valid():
            student = f.save()
            return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    return render(request, 'polls/login_form.html', {'form': f})


def quiz(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.attempted:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    # group = student.get_group()
    latest_question_list = Question.objects.filter(question_type='T1')
    if student.group == 'G1':
        latest_question_list = latest_question_list.union(Question.objects.filter(question_type='T2'))
    context = {'latest_question_list': latest_question_list, 'student' : student}
    return render(request, 'polls/quiz.html', context)



def results(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if not student.attempted:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    responses = Student_Response.objects.filter(student_id=student)
    _dict = []
    score = 0
    total = 0
    for response in responses:
        total += 1
        if response.choice_id.is_correct:
            score += 1
        _dict.append(str(response.choice_id))
    data = (student, score, total)
    return HttpResponse("Hello, world. You're at results for %s. You answered %d out of %d questions correctly." % data)


@require_POST
def submit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if not student.attempted:
        student.attempted = True
        student.save()
        for key, value in request.POST.items():
            if key.startswith('mcq_'):
                question_id = int(value.split(',')[0])
                choice_id = int(value.split(',')[1])
                question = Question.objects.get(id=question_id)
                choice_filter = Choice.objects.filter(question=question, id=choice_id)
                try:
                    choice = choice_filter[0]
                    student_response = Student_Response(student_id=student, question_id=question, choice_id=choice)
                    student_response.save()
                except Exception:
                    pass
    return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
