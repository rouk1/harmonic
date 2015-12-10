from harmonic.mixins import SeoAdmin
from modeltranslation.admin import TranslationAdmin


class SectionAdmin(SeoAdmin, TranslationAdmin):
    pass


class ArtistAdmin(TranslationAdmin):
    pass


class AlbumAdmin(SeoAdmin, TranslationAdmin):
    filter_horizontal = ('sections', 'artists',)