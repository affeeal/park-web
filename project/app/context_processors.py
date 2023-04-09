from .models import popular_tags
from .models import best_members

def base(request):
    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
