from pages.models import HomePage, Page, DefaultBackground
from django.shortcuts import render, get_object_or_404


def home(request):
    p = HomePage.get_solo()
    context = {
        'page': p,
        'background': DefaultBackground.get_solo().background,
    }
    return render(request, 'pages/home.html', context)


def page(request, slug):
    p = get_object_or_404(Page, slug=slug)
    context = {
        'page': p,
        'background': (
            p.background if p.background is not None
            else DefaultBackground.get_solo().background
        ),
    }
    return render(request, 'pages/page.html', context)
