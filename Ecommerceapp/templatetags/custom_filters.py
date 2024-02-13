# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='group_by')
def group_by(value, key):
    result = {}
    for item in value:
        result.setdefault(item[key], []).append(item)
    return result

@register.filter(name='list_to_string')
def list_to_string(value):
    return ','.join(map(str, value))