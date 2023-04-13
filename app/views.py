from django.shortcuts import render
from django.http import Http404
from app.models import Answer, Question, Tag 
from app.utils import paginate


def index(request):
    context = {
        'page': paginate(request, Question.objects.new()),
    }
    return render(request, 'index.html', context)


def hot(request):
    context = {
        'page': paginate(request, Question.objects.hot()),
    }
    return render(request, 'index.html', context)


def tag(request, tag_name):
    context = {
        'tag': Tag.objects.get(name=tag_name),
        'page': paginate(request, Question.objects.by_tag(tag_name)),
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        question=Question.objects.with_details().get(pk=question_id)
    except IndexError:
        raise Http404("Question does not exist")
    else:
        context={
            'question': question,
            'answers': Answer.objects.top_by_question(question), #type:ignore
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

