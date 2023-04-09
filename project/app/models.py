from django.db import models

questions = [
    {
        'answers': [
            {
                'author': 'Answer author',
                'id': j,
                'rating': 0,
                'text': 'Answer text',
            } for j in range(3)
        ],
        'author': 'Question author',
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
