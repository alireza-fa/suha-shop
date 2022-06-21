from django import template


register = template.Library()


@register.filter(name='range')
def range_filter(value):
    if value:
        return range(round(value))
    return range(0)
