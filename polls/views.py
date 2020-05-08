from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Question, Choice, Student, Student_Choice, Student_Question
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
    return HttpResponse("Hello, world. You're at QUIZ %s." % student.get_group())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def submit(request, student_id):
    question = get_object_or_404(Student, pk=student_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
