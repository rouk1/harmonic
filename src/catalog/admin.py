from django.utils.translation import ugettext_lazy as _
from harmonic.mixins import SeoAdmin, PublishableMixin
from modeltranslation.admin import TranslationAdmin
from renderer.widgets import MasterImageAdminMixin


class SectionAdmin(SeoAdmin, TranslationAdmin):
    pass


class ArtistAdmin(TranslationAdmin):
    search_fields = ('name', 'bio',)


class AlbumAdmin(MasterImageAdminMixin, SeoAdmin, TranslationAdmin, PublishableMixin):
    filter_horizontal = ('sections', 'artists',)
    search_fields = (
        'reference',
        'track_list',
        'description',
        'musicological_text',
        'instrument_name',
        'instrument_text',
        'press_review',
    )
    list_filter = ('sections', 'artists',)
    list_display = ('get_cover', 'reference', 'is_published',)
    list_display_links = ('get_cover', 'reference', 'is_published',)

    def get_cover(self, obj):
        '''admin image tag for easy browse'''
        t = (obj.cover.get_rendition_url(100), obj.cover.alternate_text)
        return '<img src="%s" alt="%s"/>' % t

    get_cover.allow_tags = True
    get_cover.short_description = _('cover')
