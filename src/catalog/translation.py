from catalog.models import Section
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title',)
