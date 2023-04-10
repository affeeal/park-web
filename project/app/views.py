from django.shortcuts import render
from django.http import Http404

from .models import questions 
from .models import hot_questions
from .models import tags 
from .utils import paginate


def index(request):
    context = {
        'page': paginate(request, questions, 5),
    }
    return render(request, 'index.html', context)


def hot(request):
    context = {
        'page': paginate(request, hot_questions, 5),
    }
    return render(request, 'index.html', context)


def tag(request, tag_name):
    context = {
        'tag': tags[tag_name],
        'page': paginate(request, questions, 5)
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        questions[question_id]
    except:
        raise Http404("Question not found")
        
    context = {
        'question': questions[question_id]
    }
    return render(request, 'question.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')

