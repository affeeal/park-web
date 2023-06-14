from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import Http404
from django.urls import reverse
from app.forms import AnswerForm, AskForm, LoginForm, SettingsForm, SignupForm
from app.models import Answer, Profile, Question, Tag 
from app.utils import paginate


@require_http_methods(['GET', 'POST'])
def index(request):
    context = {
        'page': paginate(request, Question.objects.newest()),
    }
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def hot(request):
    context = {
        'page': paginate(request, Question.objects.hottest()),
    }
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def tag(request, tag_name):
    context = {
        'tag': Tag.objects.get(name=tag_name),
        'page': paginate(request, Question.objects.by_tag(tag_name)),
    }
    return render(request, 'tag.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def question(request, question_id):
    try:
        question = Question.objects.with_details().get(pk=question_id)
    except IndexError:
        raise Http404("Question does not exist")
    else:
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                # TODO: ситуация, когда отвечает неавторизованный пользователь
                Answer.objects.create(
                    question=question,
                    profile=Profile.objects.by_user(request.user),
                    text=form.cleaned_data.get('text'),
                )
                return redirect(reverse('question', args=[question_id]))
        else:
            form = AnswerForm()
        context = {
            'question': question,
            'answers': Answer.objects.top_by_question(question), #type:ignore
            'form': form,
        }
        return render(request, 'question.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('next'))
            form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next'))


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
            )
            auth.login(request, user) # user is not None
            return redirect(reverse('index'))
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                profile=Profile.objects.by_user(request.user),
                title=form.cleaned_data.get('title'),
                text=form.cleaned_data.get('text'),
                # TODO: теги
            )
            return redirect(reverse('question', args=[question.id]))
    else:
        form = AskForm()
    context = {
        'form': form,
    }
    return render(request, 'ask.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = SettingsForm(initial=model_to_dict(request.user))
    context = {
        'form': form,
    }
    return render(request, 'settings.html', context)

