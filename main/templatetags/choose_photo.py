from django import template
from products.models import Photo

register = template.Library()


@register.filter(name='choose_photo')
def choose_photo(value, arg):
    try:
        value = Photo.objects.filter(product_id=arg, is_active=True, main_photo=True).first()
        return value
    except:
        return None