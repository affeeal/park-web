from app.models import Tag, Profile


def base(request):
    return {
        'popular_tags': Tag.objects.popular(), # TODO
        'best_members': Profile.objects.best(), # TODO
    }
