from catalog.models import Section
from pages.models import HomePage, HomePagePush, Page, DefaultBackground
from django.shortcuts import render, get_object_or_404


def home(request):
    p = HomePage.get_solo()
    items = []
    items.extend(Section.objects.all())
    items.extend(Page.objects.all())
    context = {
        'page': p,
        'background': DefaultBackground.get_solo().background,
        'pushes': HomePagePush.objects.all(),
        'items': items,
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
