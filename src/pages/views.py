from pages.models import HomePage, Page
from django.shortcuts import render, get_object_or_404


def page(request, slug='home'):
    if slug == 'home':
        p = HomePage.get_solo()
    else:
        p = get_object_or_404(Page, slug=slug)

    context = {
        'page': p
    }
    return render(request, 'pages/page.html', context)
