from colorfield.fields import ColorField
from django.db import models
from harmonic.mixins import SeoModel


class Section(SeoModel):
    title = models.CharField(max_length=128)
    title_color = ColorField(default='#000000')

    def __str__(self):
        return self.title