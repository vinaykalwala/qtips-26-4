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




# custom_filters.py

from django import template

register = template.Library()

@register.filter
def chunked(lst, chunk_size):
    """Custom template filter to split a list into chunks."""
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
