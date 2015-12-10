from catalog.models import HomePagePush
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from solo.admin import SingletonModelAdmin


class SeoMixin(object):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SeoMixin, self).get_fieldsets(request, obj)

        seo_fields = ('description', 'keywords',)
        for (name, fieldset) in fieldsets:
            fieldset['fields'] = [field for field in fieldset['fields'] if field not in seo_fields]
        return fieldsets + [
            ('SEO options', {
                'classes': ('collapse',),
                'fields': seo_fields,
            })
        ]


class PageAdmin(SeoMixin, TranslationAdmin):
    list_display = ('slug',)
    list_display_links = ('slug',)
    search_fields = ('slug', 'content',)


class HomePagePushAdmin(TranslationStackedInline):
    model = HomePagePush
    extra = 0


class HomePageAdmin(SeoMixin, TranslationAdmin, SingletonModelAdmin):
    inlines = [
        HomePagePushAdmin
    ]
