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
import logging

from .models import *
# from .models import Question, Choice, Student, Student_Choice, Student_Question, Student_Response, Survey_Choice, Survey_Question
from .forms import LoginForm 


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        f = LoginForm()
    else:
        f = LoginForm(request.POST)
        if f.is_valid():
            student = f.save()
            if student.name.startswith('1'):
                student.group = Student.GROUP1
            elif student.name.startswith('2'):
                student.group = Student.GROUP2
            elif student.name.startswith('3'):
                student.group = Student.GROUP3
            else:
                student.group = random.choice(
                [Student.GROUP1, Student.GROUP2, Student.GROUP3])
            student.stage = Student.STAGE1
            student.save()
            return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    print(render(request, 'polls/STAGE0/login_form.html', {'form': f}))
    return render(request, 'polls/STAGE0/login_form.html', {'form': f})


def quiz(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE2:
        return HttpResponseRedirect(reverse('polls:survey', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    latest_question_list = Question.objects.filter(
        question_type=Question.TYPE1)
    if student.group == Student.GROUP1 or student.group == Student.GROUP4:
        latest_question_list = latest_question_list.union(
            Question.objects.filter(question_type=Question.TYPE2))
    context = {'latest_question_list': latest_question_list.order_by(
        'sort_order'), 'student': student}
    return render(request, 'polls/STAGE1/quiz_dynamic_individual.html', context)


@require_POST
def quiz_log(request, student_id):
    # now = timezone.now()
    student = get_object_or_404(Student, pk=student_id)
    element_type = request.POST.get('type')
    action = request.POST.get('action')
    element_id = request.POST.get('element_id')
    if element_type == 'choice':
        choice_id = element_id.split(',')[1]
        choice = get_object_or_404(Choice, pk=choice_id)
        append = "correct" if choice.is_correct else "incorrect"
        action = action + " " + append
    # print(element_type+" "+element_id+" "+action)
    try:
        log = Log(student_id=student, element_type=element_type,
                  action=action, element_id=element_id)
        log.save()
    except Exception:
        pass
    return HttpResponse(
        json.dumps({}),
        content_type="application/json"
    )

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
            form = loader.render_to_string(
                'polls/STAGE1/create_mcq_form_wrapper.html', {})
        student.save()
    submit = loader.render_to_string(
        'polls/STAGE1/submit-quiz-button.html', {})

    response_data['append_question_list'] = loader.render_to_string(
    'polls/STAGE1/list_questions_individual.html',
    {'latest_question_list': latest_question_list.order_by('sort_order'), 'offset': 6})
    response_data['create_mcq_form'] = form
    response_data['submit'] = submit

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def survey(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    context = {'student': student}
    survey_question_list = Survey_Question.objects.filter(
        question_type=Survey_Question.TYPE1)
    if student.group != Student.GROUP1:
        survey_question_list = survey_question_list.union(
            Survey_Question.objects.filter(question_type=Survey_Question.TYPE2))
    if student.group == Student.GROUP4:
        context['extra_question_list'] = Survey_Question.objects.filter(
            question_type=Survey_Question.TYPE3).order_by('sort_order')
    if student.group == Student.GROUP5:
        context['extra_question_list'] = Survey_Question.objects.filter(
            question_type=Survey_Question.TYPE4).order_by('sort_order')
    context['survey_question_list'] = survey_question_list.order_by(
        'sort_order')
    return render(request, 'polls/STAGE2/survey.html', context)


@require_POST
def submit_survey(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    elif student.stage == Student.STAGE3:
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))
    else:
        choice_map = {
            'CHOICE1': Student_Survey_Response.CHOICE1,
            'CHOICE2': Student_Survey_Response.CHOICE2,
            'CHOICE3': Student_Survey_Response.CHOICE3,
            'CHOICE4': Student_Survey_Response.CHOICE4,
            'CHOICE5': Student_Survey_Response.CHOICE5
        }
        for key, value in request.POST.items():
            if key.startswith('survey_'):
                question_id = int(value.split(',')[0])
                survey_choice = value.split(',')[1]
                survey_choice_id = choice_map[survey_choice]
                survey_question = Survey_Question.objects.get(id=question_id)
                try:
                    student_survey_response = Student_Survey_Response(
                        student_id=student, survey_question_id=survey_question, survey_choice_id=survey_choice_id)
                    student_survey_response.save()
                except Exception:
                    logging.error("Could not save survey response for "+student)
        consent_survey = request.POST.get('consent_survey') == "True"
        choice_text = request.POST.get('choice_text', '')
        if choice_text:
            try:
                addn_text = Student_Survey_Additional_Text(student_id = student, text = choice_text)
                addn_text.save()
            except Exception:
                    logging.error("Could not save survey response additional text for "+student)
        student.consent_survey = consent_survey
        student.stage = Student.STAGE3
        student.save()
        return HttpResponseRedirect(reverse('polls:results', args=(student.id,)))


def results(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE1:
        return HttpResponseRedirect(reverse('polls:quiz', args=(student.id,)))
    elif student.stage == Student.STAGE2:
        return HttpResponseRedirect(reverse('polls:survey', args=(student.id,)))
    responses = Student_Response.objects.filter(student_id=student)
    score = 0
    total = 0
    for response in responses:
        total += 1
        if response.choice_id.is_correct:
            score += 1
    context = {'student': student, 'score': str(score), 'total': str(total)}
    print(context)
    return render(request, 'polls/STAGE3/results.html', context)


@require_POST
def submit_quiz(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.stage == Student.STAGE2:
        return HttpResponseRedirect(reverse('polls:survey', args=(student.id,)))
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
            student_consent_create_mcq = request.POST.get(
                'consent_create_mcq') == "True"
            student.consent_create_mcq = student_consent_create_mcq
            student_question = Student_Question()
            student_question.question_text = request.POST.get('student_question')
            student_question.by_student = student
            student_question.explanation_text = request.POST.get('student_explanation')
            student_question.save()
            for i in range(1,5):
                if request.POST.get('student_choice_'+str(i)) != '':
                    student_choice = Student_Choice()
                    student_choice.choice_text = request.POST.get('student_choice_'+str(i))
                    student_choice.question = student_question
                    if i == 1:
                        student_choice.is_correct = True
                    else:
                        student_choice.is_correct = False
                    student_choice.save()
        student.stage = Student.STAGE2
        student.save()
    return HttpResponseRedirect(reverse('polls:survey', args=(student.id,)))
