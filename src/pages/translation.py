from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from pages.models import Page, HomePage, HomePagePush


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'seo_description',)


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('content', 'seo_description',)


@register(HomePagePush)
class HomePagePushTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)
