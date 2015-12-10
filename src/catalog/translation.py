from catalog.models import Section, Artist
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = ('bio',)