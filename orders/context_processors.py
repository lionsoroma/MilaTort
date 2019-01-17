from orders.models import Order
from products.models import Photo


def get_basket_content(request):
    if 'referer_path' in request.session:
        referer_path = request.session['referer_path']
    small_photos_in_order = []
    sums_order = []
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    client = None
    if request.user.is_active:
        client = request.user.client
    orders = Order.objects.filter(client=client, present_in_basket=True, status_of_order='new', session_key=session_key,
                                product__category_plus_type_product__category__is_staff=False).order_by('dates_order')
    count_orders_in_basket = orders.count()
    for order_in_basket in orders:
        price = order_in_basket.product.price
        weight_or_pcs = order_in_basket.weight_or_pcs
        sum_one = weight_or_pcs * (price - (price/100 * order_in_basket.discount_total))
        sums_order.append(sum_one)
    total_amount = sum(sums_order)
    for order in orders:
        small_photos_in_order.append(Photo.objects.filter(product_id=order.product_id, is_active=True, main_photo=True).first())
    if not count_orders_in_basket or count_orders_in_basket == 0:
        visible_off = 'visible_off'
    return locals()
