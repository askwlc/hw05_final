from django.conf import settings
from django.core.paginator import Paginator


def paginate_page(request, posts):
    paginator = Paginator(posts, settings.NUMBER_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
