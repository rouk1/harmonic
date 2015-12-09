from catalog.widgets import SimpleMDEEditor
from django.db import models

class MarkdownField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        defaults['widget'] = SimpleMDEEditor
        return super(MarkdownField, self).formfield(**defaults)

class SeoModel(models.Model):
    description = models.TextField()
    keywords = models.TextField()

    class Meta:
        abstract = True

class Page(SeoModel):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    content = MarkdownField()


class Section(models.Model):
    title = models.CharField(max_length=128)
