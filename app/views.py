from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.urls import reverse
from app.forms import AnswerForm, AskForm, LoginForm, SettingsForm, SignupForm
from app.models import Answer, AnswerLike, Question, QuestionLike, Tag 
from app.utils import paginate


@require_GET
def index(request):
    context = {
        'page': paginate(request, Question.objects.newest(request.user))
    }
    return render(request, 'index.html', context)


@require_GET
def hot(request):
    context = {
        'page': paginate(request, Question.objects.hottest(request.user)),
    }
    return render(request, 'index.html', context)


@require_GET
def tag(request, tag_name):
    context = {
        'tag': Tag.objects.get(name=tag_name),
        'page': paginate(
            request, Question.objects.by_tag(request.user, tag_name)
        ),
    }
    return render(request, 'tag.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def question(request, question_id):
    try:
        question = Question.objects.with_details(request.user).get(pk=question_id)
    except IndexError:
        raise Http404("Question does not exist")
    
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            # TODO: ситуация, когда отвечает неавторизованный пользователь
            Answer.objects.create(
                question=question,
                profile=request.user.profile,
                text=form.cleaned_data.get('text'),
            )
            return redirect(reverse('question', args=[question_id]))
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'is_author': question.profile == request.user.profile,
        'answers': Answer.objects.top(request.user, question),
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
                profile=request.user.profile,
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

@require_POST
def question_vote(request):
    try:
        question_id = int(request.POST.get('question_id'))
        question_vote = int(request.POST.get('question_vote'))
    except ValueError:
        return JsonResponse({}) # TODO
    
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: #type:ignore
        return JsonResponse({}) # TODO
    
    try:
        question_like = QuestionLike.objects.get( #type:ignore
            profile=request.user.profile,
            question=question,
        )
        
        if question_like.value != question_vote:
            question_like.value = question_vote
            question_like.save()
        else:
            question_like.delete()
    except QuestionLike.DoesNotExist: #type:ignore
        QuestionLike.objects.create( #type:ignore
            profile=request.user.profile,
            question=question,
            value=question_vote,
        )
        
    return JsonResponse({
        'rating': Question.objects.with_details(request.user)
                          .get(pk=question_id).rating
    })
    
@require_POST
def answer_vote(request):
    try:
        answer_id = int(request.POST.get('answer_id'))
        answer_vote = int(request.POST.get('answer_vote'))
    except ValueError:
        return JsonResponse({}) # TODO
    
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist: #type:ignore
        return JsonResponse({}) # TODO
    
    try:
        answer_like = AnswerLike.objects.get( #type:ignore
            profile=request.user.profile,
            answer=answer,
        )
        
        if answer_like.value != answer_vote:
            answer_like.value = answer_vote
            answer_like.save()
        else:
            answer_like.delete()
    except AnswerLike.DoesNotExist: #type:ignore
        AnswerLike.objects.create( #type:ignore
            profile=request.user.profile,
            answer=answer,
            value=answer_vote,
        )
        
    return JsonResponse({
        'rating': Answer.objects.with_details(
            request.user, answer.question
        ).get(pk=answer_id).rating
    })


@require_POST
def answer_correct(request):
    try:
        answer_id = int(request.POST.get('answer_id'))
    except ValueError:
        return
    
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist: #type:ignore
        return
    
    answer.correct = not answer.correct
    answer.save()
    
    return
