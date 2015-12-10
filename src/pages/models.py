from django.db import models
from harmonic.fields import MarkdownField
from harmonic.mixins import SeoModel
from solo.models import SingletonModel


class Page(SeoModel):
    slug = models.SlugField()
    title = models.CharField(max_length=128)
    content = MarkdownField()

    class Meta:
        verbose_name = 'simple page'
        verbose_name_plural = 'simple pages'

    def __unicode__(self):
        return 'Page: {}'.format(self.slug)


class HomePage(SeoModel, SingletonModel):
    content = MarkdownField()


class HomePagePush(models.Model):
    home_page = models.ForeignKey('HomePage')
    title = models.CharField(max_length=128)
    content = MarkdownField()
