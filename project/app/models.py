from django.db import models

questions = [
    {
        'answers': [
            {
                'author': 'nickname',
                'id': j,
                'rating': 0,
                'text': 'Answer text',
            } for j in range(3)
        ],
        'author': 'nickname',
        'id': i,
        'rating': 0,
        'tags': [
            {
                'name': f'tag-name-{j}',
                'usages': 0,
            } for j in range(3)
        ],
        'text': 'Question text',
        'title': 'Question title',
    } for i in range(3)
]

hot_questions = [
    {
        'answers': [
            {
                'author': 'nickname',
                'id': j,
                'rating': 0,
                'text': 'Answer text',
            } for j in range(3)
        ],
        'author': 'nickname',
        'id': i,
        'rating': 0,
        'tags': [
            {
                'name': f'tag-name-{j}',
                'usages': 0,
            } for j in range(3)
        ],
        'text': 'Hot question text',
        'title': 'Hot question title',
    } for i in range(3)
]

tags = {
    f'tag-name-{i}': {
        'name': f'tag-name-{i}',
        'usages': 0,
    } for i in range(5)
}

popular_tags = [
    {
        'name': f'tag-name-{i}',
        'usages': 0,
    } for i in range(5)
]

best_members = [
    {
        'nickname': f'nickname-{i}',
    } for i in range(5)
]
