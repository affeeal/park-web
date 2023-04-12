from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def question_key(question):
    likes = QuestionLike.objects.filter(question=question)
    rating = 0
    for like in likes:
        if like.vote==True:
            rating+= 1
        elif like.vote==False:
            rating-=1
    return rating

class QuestionManager(models.Manager):
    def by_tag(self, name):
        return self.filter(tags__name=name)

    def new(self):
        return self.order_by("time")

    def hot(self):
        global question_key
        return sorted(self.all(), key=question_key, reverse=True)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    title = models.TextField(max_length=150)
    text = models.TextField(max_length=15000)
    tags = models.ManyToManyField("Tag", blank=True)
    
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=15000)

    def __str__(self):
        return self.text


class TagManager(models.Manager):
    def popular(self):
        def popular_key(tag):
            return Question.objects.filter(tags__name=tag.name).count()
        return sorted(self.all(), key=popular_key, reverse=True)[:10]


class Tag(models.Model):
    name = models.CharField(max_length=15)

    objects = TagManager()

    def __str__(self):
        return self.name


class ProfileManager(models.Manager):
    def best(self):
        def best_key(profile):
            answers=Answer.objects.filter(user=profile.user)
            likes=AnswerLike.objects.filter(answer__in=answers)
            rating=0
            for like in likes:
                if like.correct==True:
                    rating+=1
            return rating
        return sorted(self.all(), key=best_key, reverse=True)[:10]
        


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to="uploads/",
        default="static/img/avatar.png")
    
    objects = ProfileManager()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField(null=True)


class QuestionLike(Like):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    

class AnswerLike(Like):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer.text

