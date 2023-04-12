from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class QuestionManager(models.Manager):
    def by_tag(self, name):
        return self.filter(tags__name=name)

    def new(self):
        return self.order_by("time")

    def hot(self):
        pass


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
        pass # TODO


class Tag(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class ProfileManager(models.Manager):
    def best(self):
        pass # TODO


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to="uploads/",
        default="static/img/avatar.png")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField(null=True)


class QuestionLike(Like):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    

class AnswerLike(Like):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
