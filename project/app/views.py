from django.shortcuts import render
from .models import questions 
from .models import tags 


def index(request):
    context = {
        'questions': questions,
    }
    return render(request, 'index.html', context)


def hot(request):
    return render(request, 'index.html') # page to return?


def tag(request, tag_name):
    context = {
        'tag': tags[tag_name],
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    context = {
        'question': questions[question_id] # handle errors
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
