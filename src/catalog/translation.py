from catalog.models import Section, Artist, Album
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'seo_description',
    )


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = ('bio',)


@register(Album)
class AlbumTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'musicological_text',
        'instrument_name',
        'instrument_text',
        'press_review',
        'seo_description',
    )
