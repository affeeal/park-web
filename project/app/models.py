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
        'text': f'Question #{i} text',
        'title': f'Question #{i} title',
    } for i in range(100)
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
        'text': f'Hot question #{i} text',
        'title': f'Hot question #{i} title',
    } for i in range(100)
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
