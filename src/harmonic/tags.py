import markdown2
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(value):
    return mark_safe(markdown2.markdown(value))


@register.filter('klass')
def klass(obj):
    return obj.__class__.__name__
