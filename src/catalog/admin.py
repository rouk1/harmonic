from django.utils.translation import ugettext_lazy as _
from harmonic.mixins import SeoAdmin, PublishableMixin
from modeltranslation.admin import TranslationAdmin
from renderer.widgets import MasterImageAdminMixin


class SectionAdmin(MasterImageAdminMixin, SeoAdmin, TranslationAdmin):
    list_display = ('title', 'get_background',)
    list_display_links = ('title', 'get_background',)

    def get_background(self, obj):
        '''admin image tag for easy browse'''
        t = (obj.background.get_rendition_url(100), obj.background.alternate_text)
        return '<img src="%s" alt="%s"/>' % t

    get_background.allow_tags = True
    get_background.short_description = _('background')


class ArtistAdmin(MasterImageAdminMixin, TranslationAdmin):
    search_fields = ('name', 'bio',)
    list_display = ('get_photo', 'name',)
    list_display_links = ('get_photo', 'name',)

    def get_photo(self, obj):
        '''admin image tag for easy browse'''
        t = (obj.photo.get_rendition_url(100), obj.photo.alternate_text)
        return '<img src="%s" alt="%s"/>' % t

    get_photo.allow_tags = True
    get_photo.short_description = _('photo')


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
