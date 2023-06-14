from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import Http404
from django.urls import reverse
from app.forms import AnswerForm, AskForm, LoginForm, SettingsForm, SignupForm
from app.models import Answer, Profile, Question, Tag 
from app.utils import paginate


def index(request):
    context = {
        'page': paginate(request, Question.objects.newest()),
    }
    return render(request, 'index.html', context)


def hot(request):
    context = {
        'page': paginate(request, Question.objects.hottest()),
    }
    return render(request, 'index.html', context)


def tag(request, tag_name):
    context = {
        'tag': Tag.objects.get(name=tag_name),
        'page': paginate(request, Question.objects.by_tag(tag_name)),
    }
    return render(request, 'tag.html', context)


@login_required
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
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next'))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.nickname = form.cleaned_data.get('nickname')
            # TODO: загрузка аватара
            user.save()
            user = auth.authenticate(
                username=user.username,
                password=form.cleaned_data.get('password1')
            )
            # user is not None
            auth.login(request, user)
            return redirect(reverse('index'))
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
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
def settings(request):
    if request.method == 'POST':
        # обновляем данные для user и ассоциированного с ним profile
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.profile.nickname = form.cleaned_data.get('nickname')
            # TODO: аватар
            user.profile.save()
    else:
        form = SettingsForm(initial={
            'username': request.user.username,
            'nickname': Profile.objects.by_user(request.user).nickname,
            'email': request.user.email,
            # TODO: аватар
        })
    context = {
        'form': form,
    }
    return render(request, 'settings.html', context)

