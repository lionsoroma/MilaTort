from django import template

register = template.Library()


@register.simple_tag(name='get_full_discount')
def get_full_discount(discount, user):
    if discount:
        if user.is_authenticated:
            full_discount = int(discount + user.client.discount_client)
            return full_discount
        else:
            return discount
    else:
        return 0
