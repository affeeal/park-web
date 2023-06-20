from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.auth.models import AnonymousUser, User
from django.dispatch import receiver
from django.utils import timezone


class ProfileManager(models.Manager):
    # профили, написавшие больше всего ответов
    def best(self):
        return self.annotate(
            models.Count('answer')
        ).order_by('-answer__count')[:10]
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, default='avatar.png',
                               upload_to='avatars/%Y/%m/%d/')
    
    objects = ProfileManager()

    def __str__(self):
        return self.user.username #type:ignore


@receiver(models.signals.post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class TagManager(models.Manager):
    # теги, употреблявшиеся больше всего раз
    def popular(self):
        return self.annotate(
            models.Count('question')
        ).order_by('-question__count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=15)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    # вопросы с рейтингом и числом ответов
    def with_details(self, user):
        votes = QuestionLike.objects.filter( #type:ignore
            question=models.OuterRef('pk')
        )

        all_votes = votes.values('question').annotate(
            value_sum=models.Sum('value')
        ).values('value_sum')[:1]

        questions = self.annotate(
            models.Count('answer', distinct=True),
            rating=Coalesce(models.Subquery(all_votes), 0),
        )

        if isinstance(user, AnonymousUser):
            return questions
        else:
            logged_in_user_votes = votes.filter(
                profile=user.profile,
            ).values('question').annotate(
                value_sum=models.Sum('value')
            ).values('value_sum')[:1]
            
            return questions.annotate(
                logged_in_user_vote=Coalesce(
                    models.Subquery(logged_in_user_votes),
                    0,
                )
            )
        
    # вопросы по тегу
    def by_tag(self, user, tag_name):
        return self.with_details(user).filter(tags__name=tag_name)

    # новейшие вопросы
    def newest(self, user):
        return self.with_details(user).order_by('-time')

    # вопросы с наибольшим рейтингом
    def hottest(self, user):
        return self.with_details(user).order_by('-rating')


class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    title = models.TextField(max_length=160)
    text = models.TextField(max_length=8000)
    tags = models.ManyToManyField(Tag, blank=True)
    
    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def with_details(self, user, question):
        votes = AnswerLike.objects.filter( #type:ignore
            answer=models.OuterRef('pk')
        )

        ratings = votes.values('answer').annotate(
            value_sum=models.Sum('value')
        ).values('value_sum')[:1]

        answers = self.filter(
            question=question
        ).annotate(
            rating=Coalesce(models.Subquery(ratings), 0),
        )

        # возвращаем ответы, если текущий пользователь не авторизован
        if isinstance(user, AnonymousUser):
            return answers
        
        # дополняем ответы лайками текущего пользователя
        user_votes = votes.filter(
            profile=user.profile,
        ).values('answer').annotate(
            value_sum=models.Sum('value')
        ).values('value_sum')[:1]
        
        return answers.annotate(
            user_vote=Coalesce(models.Subquery(user_votes), 0)
        )


    # ответы на вопрос question, отсортированные по rating
    def top(self, user, question):
        return self.with_details(user, question).order_by('-rating')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    correct = models.BooleanField(default=False) #type:ignore

    objects = AnswerManager()

    def __str__(self):
        return self.question.title #type:ignore


class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(-1, 'down'), (1, 'up')]) #type:ignore

    def __str__(self):
        return ('up' if (self.value == 1) else 'down') \
            + ' from ' + self.profile.user.username \
            + ' to question #' + str(self.question.pk) #type:ignore
    
class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(-1, 'down'), (1, 'up')]) #type:ignore

    def __str__(self):
        return ('up' if (self.value == 1) else 'down') \
            + ' from ' + self.profile.user.username \
            + ' to answer #' + str(self.answer.pk) #type:ignore
