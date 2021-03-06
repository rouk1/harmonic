from django.db import models
from harmonic.fields import MarkdownField
from harmonic.mixins import SeoModel
from solo.models import SingletonModel


class DefaultBackground(SingletonModel):
    background = models.ForeignKey(
        'renderer.MasterImage',
        blank=True,
        null=True
    )


class Page(SeoModel):
    slug = models.SlugField()
    title = models.CharField(max_length=128)
    background = models.ForeignKey(
        'renderer.MasterImage',
        blank=True,
        null=True
    )
    content = MarkdownField()

    class Meta:
        verbose_name = 'simple page'
        verbose_name_plural = 'simple pages'

    def __unicode__(self):
        return 'Page: {}'.format(self.slug)


class HomePage(SeoModel, SingletonModel):
    content = MarkdownField()


class HomePagePush(models.Model):
    # FIXME add a published boolean
    # put them in the home page
    home_page = models.ForeignKey('HomePage')
    title = models.CharField(max_length=128)
    content = MarkdownField()
