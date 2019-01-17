from django import template
from main.models import Client

register = template.Library()


@register.filter(name='discount_client')
def discount_client(value, arg):
    try:
        value = Client.objects.get(product_id=arg).discount_total
        return value
    except:
        return None
