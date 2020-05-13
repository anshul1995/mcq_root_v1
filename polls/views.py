from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

import random
import codecs
import json

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
            student.group = random.choice(
                [Student.GROUP1, Student.GROUP2, Student.GROUP3])
            student.stage = Student.STAGE2
            student.save()
            return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    print(render(request, 'polls/login_form.html', {'form': f}))
    return render(request, 'polls/login_form.html', {'form': f})


@require_http_methods(['GET', 'POST'])
def info(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE2:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    if request.method == 'POST':
        student.stage = Student.STAGE2
        # if student.group == Student.GROUP3:
        #     if request.POST['G3_choice'] == Student.GROUP4:
        #         student.group = Student.GROUP4
        #     else:
        #         student.group = Student.GROUP5
        student.save()
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    return render(request, 'polls/info.html', {'student': student})


def quiz(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:info', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    latest_question_list = Question.objects.filter(
        question_type=Question.TYPE1)
    if student.group == Student.GROUP1 or student.group == Student.GROUP4:
        latest_question_list = latest_question_list.union(
            Question.objects.filter(question_type=Question.TYPE2))
    context = {'latest_question_list': latest_question_list, 'student': student}
    return render(request, 'polls/quiz_dynamic.html', context)


@require_POST
def g3_choice(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    response_data = {}
    latest_question_list = Question.objects.none()
    form = ''
    choice = request.POST.get('choice')
    if student.group == Student.GROUP3:
        if choice == Student.GROUP4:
            student.group = Student.GROUP4
            latest_question_list = Question.objects.filter(
                question_type=Question.TYPE2)
        else:
            student.group = Student.GROUP5
            form = loader.render_to_string('polls/create_mcq_form.html', {})
        student.save()
    submit = loader.render_to_string('polls/submit-quiz-button.html', {})

    response_data['append_question_list'] = loader.render_to_string(
        'polls/list_questions.html', {'latest_question_list': latest_question_list, 'offset': 6})
    response_data['create_mcq_form'] = form
    response_data['submit'] = submit

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )



def results(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:info', args=(student.id,)))
    elif student.stage == Student.STAGE2:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    responses = Student_Response.objects.filter(student_id=student)
    score = 0
    total = 0
    for response in responses:
        total += 1
        if response.choice_id.is_correct:
            score += 1
    context = {'student': student, 'score': str(score), 'total': str(total)}
    print(context)
    return render(request, 'polls/results.html', context)


@require_POST
def submit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:info', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    else:
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
                    choice.votes += 1
                    choice.save()
                except Exception:
                    pass
        if student.group == Student.GROUP2 or student.group == Student.GROUP5:
            student_question = Student_Question()
            student_question.question_text = request.POST['student_question']
            student_question.by_student = student
            student_question.explanation_text = request.POST['student_explanation']
            student_question.save()
            for i in range(1,6):
                if request.POST['student_choice_'+str(i)] != '':
                    student_choice = Student_Choice()
                    student_choice.choice_text = request.POST['student_choice_'+str(i)]
                    student_choice.question = student_question
                    if i == 1:
                        student_choice.is_correct = True
                    else:
                        student_choice.is_correct = False
                    student_choice.save()
        student.stage = Student.STAGE3
        student.save()

    return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
