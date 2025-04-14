from django import template

register = template.Library()

@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)


@register.filter
def to_range(value, arg):
    """
    Usage: {% for i in 1|to_range:5 %}
    Loops from 1 to 5 (inclusive)
    """
    return range(int(value), int(arg) + 1)