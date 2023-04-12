from django.shortcuts import render
from django.http import Http404
from .utils import paginate
from . import models


def index(request):
    context = {
        'page': paginate(request, models.Question.objects.new(), 5),
    }
    return render(request, 'index.html', context)


def hot(request):
    context = {
        'page': paginate(request, models.Question.objects.hot(), 5),
    }
    return render(request, 'index.html', context)


def tag(request, tag_name):
    context = {
        'tag': tag_name,
        'page': paginate(request, models.Question.objects.by_tag(tag_name), 5),
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        context = {
            'question': questions[question_id],
        }
    except IndexError:
        raise Http404("Question does not exist")
    else:
        return render(request, 'question.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')

