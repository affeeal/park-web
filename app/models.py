from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# профили, написавшие больше всего ответов
class ProfileManager(models.Manager):
    def best(self):
        return self.annotate(models.Count('answer')).order_by('-answer__count')[:10]
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO разобраться с аватарками
    avatar = models.FileField(
        upload_to="uploads/",
        default="static/img/avatar.png"
    )
    
    objects = ProfileManager()

    def __str__(self):
        return self.user.username #type:ignore


# теги, употреблявшиеся больше всего раз
class TagManager(models.Manager):
    def popular(self):
        return self.annotate(models.Count('question')).order_by('-question__count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=15)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    # вопросы с рейтингом и числом ответов
    def with_details(self):
        return self.annotate(
            models.Count('answer', distinct=True)
        ).annotate(
            rating=models.Sum('questionlike__value')
        )

    # вопросы по тегу
    def by_tag(self, name):
        return self.with_details().filter(tags__name=name)

    # новейшие вопросы
    def new(self):
        return self.with_details().order_by('-time')

    # вопросы с наибольшим рейтингом
    def hot(self):
        return self.with_details().order_by('-rating')


class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    title = models.TextField(max_length=150)
    text = models.TextField(max_length=15000)
    tags = models.ManyToManyField(Tag, blank=True)
    
    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    # ответы с рейтингом
    def with_details(self):
        return self.annotate(rating=models.Sum('answerlike__value'))

    # ответы на определённый вопрос, отсортировнные по рейтингу
    def top_by_question(self, question):
        return self.with_details().filter(question=question).order_by('-rating')


class Answer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    text=models.TextField(max_length=15000)

    objects=AnswerManager()

    def __str__(self):
        return self.question.title #type:ignore


class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(-1, 'down'), (1, 'up')]) #type:ignore

    
class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(-1, 'down'), (1, 'up')]) #type:ignore

    
# если существует, значит correct=true
class AnswerCorrect(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
