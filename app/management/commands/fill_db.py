from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Question, Answer, QuestionLike, AnswerLike, Tag, Profile


class Command(BaseCommand):
    help = "fills db with data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs="?", default=1, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        users = [
            User(
                username=f'user{i}',
                password='password',
                email=f'user{i}@user{i}.ru',
            ) for i in range(ratio)
        ]
        User.objects.bulk_create(users)

        tags = [
            Tag(
                name=f'tag-{i}',
            ) for i in range(ratio)
        ]
        Tag.objects.bulk_create(tags)

        questions=[]
        for i in range(ratio):
            _questions=[
                Question(
                    title=f'Question #{i*10+j} title',
                    text=f'Question #{i*10+j} text',
                    user=users[i],
                ) for j in range(10)
            ]
            for question in questions:
                question.tags.add(tags[i])
            questions.extend(_questions)
        Question.objects.bulk_create(questions)

        answers=[]
        for i in range(len(questions)):
            _answers=[
                Answer(
                    question=questions[i],
                    user=questions[i].user,
                    text=f'Answer #{j} to Question #{i} text',
                ) for j in range(10)
            ]
            answers.extend(_answers)
        Answer.objects.bulk_create(answers)
