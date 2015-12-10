from harmonic.mixins import SeoAdmin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from pages.models import HomePagePush
from solo.admin import SingletonModelAdmin


class PageAdmin(SeoAdmin, TranslationAdmin):
    list_display = ('slug',)
    list_display_links = ('slug',)
    search_fields = ('slug', 'content',)


class HomePagePushAdmin(TranslationStackedInline):
    model = HomePagePush
    extra = 0


class HomePageAdmin(SeoAdmin, TranslationAdmin, SingletonModelAdmin):
    inlines = [
        HomePagePushAdmin
    ]
