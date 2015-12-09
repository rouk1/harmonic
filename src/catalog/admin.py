from modeltranslation.admin import TranslationAdmin


class PageAdmin(TranslationAdmin):
    list_display = ('slug', )
    list_display_links = ('slug', )
    search_fields = ('slug', 'content', 'title', )
