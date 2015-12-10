from catalog.models import Page, HomePage, HomePagePush
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(HomePagePush)
class HomePagePushTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)
