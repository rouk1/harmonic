from catalog.models import Album
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from pages.models import Page, HomePage, HomePagePush


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(HomePagePush)
class HomePagePushTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(Album)
class AlbumTranslationOptions(TranslationOptions):
    fields = ('description', 'musicological_text', 'instrument_text', 'press_review',)
