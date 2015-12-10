from django.db import models
from harmonic.widgets import SimpleMDEEditor


class MarkdownField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        defaults['widget'] = SimpleMDEEditor
        return super(MarkdownField, self).formfield(**defaults)
