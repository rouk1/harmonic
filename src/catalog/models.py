from catalog.widgets import SimpleMDEEditor
from django.db import models
from solo.models import SingletonModel


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
    title = models.CharField(max_length=128)
    content = MarkdownField()

    def __unicode__(self):
        return 'Page: {}'.format(self.slug)


class Section(models.Model):
    title = models.CharField(max_length=128)


class HomePage(SeoModel, SingletonModel):
    content = MarkdownField()


class HomePagePush(models.Model):
    home_page = models.ForeignKey('HomePage')
    title = models.CharField(max_length=128)
    content = MarkdownField()
