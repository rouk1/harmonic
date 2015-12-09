from catalog.models import Page
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

