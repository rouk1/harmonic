from django.forms import Textarea
from django.utils.safestring import mark_safe

__author__ = 'rouk1'


class SimpleMDEEditor(Textarea):
    class Media:
        js = (
            '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
            'admin/js/editor.js',
        )
        css = {
            'all': (
                '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
                'admin/css/editor.css',
            )
        }

    def render(self, name, value, attrs=None):
        final_attrs = {'class': 'simple-mde-editor'}
        if attrs is not None:
            final_attrs.update(attrs)
        output = super(SimpleMDEEditor, self).render(
            name,
            value,
            attrs=final_attrs
        )

        output = '<div class="simple-mde-editor-wrapper">{}</div>'.format(
            output
        )
        return mark_safe(output)
