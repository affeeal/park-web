from app.models import Tag, Profile


def base(request):
    return {
        'popular_tags': Tag.objects.all(), # TODO
        'best_members': Profile.objects.all(), # TODO
    }
