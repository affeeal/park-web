from django.core.paginator import Paginator

def represents_int(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


def paginate(request, object_list, per_page=5, on_each_side=3, on_ends=2):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    
    if page_number is None or not represents_int(page_number) \
       or int(page_number) < 1 or int(page_number) > paginator.num_pages: #type:ignore
        page_number = 1

    return {
        'obj': paginator.get_page(page_number),
        'elided_range': paginator.get_elided_page_range(number=page_number,
                                                        on_each_side=on_each_side,
                                                        on_ends=on_ends),
        'ellipsis': paginator.ELLIPSIS,
    }
