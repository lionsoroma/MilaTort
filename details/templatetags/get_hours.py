from django import template


register = template.Library()


@register.filter(name='get_hours')
def get_hours(td):
    if td:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return '{} год.'.format(hours)
        else:
            return None
    else:
        return None
