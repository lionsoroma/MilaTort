from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set_global_context(context, key, value):
    context.dicts[0][key] = value
    return ''
