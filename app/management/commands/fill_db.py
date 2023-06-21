import random
import lorem
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app import models


class Command(BaseCommand):
    help = "fills db with data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs="?", default=1, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        users = []
        for i in range(ratio):
            users.append(
                User(
                    username=f'user{i}',
                    first_name='User',
                    last_name=f'no. {i}',
                    email=f'user{i}@user{i}.ru',
                )
            ) 
            users[i].set_password('password')
        User.objects.bulk_create(users)

        profiles = [
            models.Profile(
                user=users[i],
            ) for i in range(ratio)
        ]
        models.Profile.objects.bulk_create(profiles)

        tags = [
            models.Tag(
                name=f'tag-{i}',
            ) for i in range(ratio)
        ]
        models.Tag.objects.bulk_create(tags)

        questions=[
            models.Question(
                title=lorem.get_sentence(),
                text=lorem.get_paragraph(count=random.randint(1, 3)),
                profile=profiles[random.randint(0, ratio-1)],
            ) for _ in range(ratio*10)
        ]
        models.Question.objects.bulk_create(questions)
        for question in questions:
            count=random.randint(0, 3) # TODO
            for _ in range(count):
                question.tags.add(tags[random.randint(0, ratio-1)]) #type:ignore

        questionlikes=[]
        for _ in range(ratio*100):
            value=random.randint(-1, 1)
            if value==0: # не храним в базе пустые оценки
                continue
            questionlikes.append(
                models.QuestionLike(
                    profile=profiles[random.randint(0, ratio-1)],
                    question=questions[random.randint(0, ratio*10-1)],
                    # проблема дублирования
                    value=value,
                )
            )
        models.QuestionLike.objects.bulk_create(questionlikes) #type:ignore

        answers=[
            models.Answer(
                profile=profiles[random.randint(0, ratio-1)],
                question=questions[random.randint(0, ratio*10-1)],
                text=lorem.get_paragraph(count=random.randint(1, 3)),
            ) for _ in range(ratio*100)
        ]
        models.Answer.objects.bulk_create(answers) #type:ignore

        answerlikes=[]
        for _ in range(ratio*100):
            value=random.randint(-1, 1)
            if value==0: # не храним в базе пустые оценки
                continue
            answerlikes.append(
                models.AnswerLike(
                    profile=profiles[random.randint(0, ratio-1)],
                    answer=answers[random.randint(0, ratio*100-1)],
                    # проблема дублирования
                    value=value,
                )
            )
        models.AnswerLike.objects.bulk_create(answerlikes) #type:ignore

        answercorrects=[]
        for _ in range(ratio*100):
            if random.randint(0, 1)==0: # не храним в базе пустые оценки
                continue
            answercorrects.append(
                models.AnswerCorrect(
                    profile=profiles[random.randint(0, ratio-1)],
                    answer=answers[random.randint(0, ratio*100-1)],
                )
            )
        models.AnswerCorrect.objects.bulk_create(answercorrects) #type:ignore

