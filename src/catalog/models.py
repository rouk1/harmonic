from colorfield.fields import ColorField
from django.db import models
from harmonic.fields import MarkdownField
from harmonic.mixins import SeoModel


class Section(SeoModel):
    title = models.CharField(max_length=128)
    title_color = ColorField(default='#000000')

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=128)
    bio = MarkdownField()

    def __str__(self):
        return self.name

class Album(SeoModel):
    is_published = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    reference = models.CharField(max_length=32)
    sections = models.ManyToManyField('Section')
    artists = models.ManyToManyField('Artist')
    itunes_url = models.URLField()
    is_digital_release = models.BooleanField(default=False)
    description = MarkdownField()
    musicological_text = MarkdownField()
    instrument_name = models.CharField(max_length=255)
    instrument_text = MarkdownField()
    track_list = MarkdownField()
    press_review = MarkdownField()

    def __str__(self):
        return '{} - {}'.format(self.reference, self.title)
