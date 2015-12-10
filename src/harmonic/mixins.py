from django.db import models


class SeoModel(models.Model):
    seo_description = models.TextField()
    seo_keywords = models.TextField()

    class Meta:
        abstract = True


class SeoAdmin(object):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SeoAdmin, self).get_fieldsets(request, obj)

        seo_fields = ('seo_description', 'seo_keywords',)
        for (name, fieldset) in fieldsets:
            fieldset['fields'] = [field for field in fieldset['fields'] if field not in seo_fields]
        return fieldsets + [
            ('SEO options', {
                'classes': ('collapse',),
                'fields': seo_fields,
            })
        ]

class PublishableMixin(object):
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    make_published.short_description = 'Mark selected items as published'

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    make_unpublished.short_description = 'Mark selected items as unpublished'