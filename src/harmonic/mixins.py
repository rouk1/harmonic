from django.db import models


class SeoModel(models.Model):
    description = models.TextField()
    keywords = models.TextField()

    class Meta:
        abstract = True


class SeoAdmin(object):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SeoAdmin, self).get_fieldsets(request, obj)

        seo_fields = ('description', 'keywords',)
        for (name, fieldset) in fieldsets:
            fieldset['fields'] = [field for field in fieldset['fields'] if field not in seo_fields]
        return fieldsets + [
            ('SEO options', {
                'classes': ('collapse',),
                'fields': seo_fields,
            })
        ]