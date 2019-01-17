from .forms import OrderListForm
from products.models import Photo
from orders.models import Order
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone


def convert_strNone_None(input_value):
    if input_value:
        if input_value.isdigit():
            return input_value
        else:
            if input_value.lower() == 'none':
                return None
            else:
                ValueError("input value should be 'none' or decimal of str wrapper")
    else:
        return input_value


def convert_trueTrue_falseFalse(input_value):
    if input_value.lower() == 'false':
        return False
    elif input_value.lower() == 'true':
        return True
    else:
        raise ValueError("input value should be 'false' or 'true' as str type")


def order(request):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        order_list_form = OrderListForm(request.POST or None)
        if order_list_form.is_valid():
            do_remove = convert_trueTrue_falseFalse(request.POST.get('do_remove'))
            order_delete_id = request.POST.get('order_delete')
            change_weight_or_pcs_order = convert_strNone_None(request.POST.get('change_weight_or_pcs_order'))
            product = order_list_form.cleaned_data['product']
            client = None
            if request.user.is_active:
                client = request.user.client
            weight_or_pcs = order_list_form.cleaned_data['weight_or_pcs']
            if not do_remove:
                if product.unit == 'kg':
                    if change_weight_or_pcs_order:
                        update_order = Order.objects.get(id=change_weight_or_pcs_order)
                        if update_order.DoesNotExist:
                            update_order.weight_or_pcs = weight_or_pcs
                            update_order.save()
                        else:
                            new_order = Order.objects.create(session_key=session_key, client=client,
                                                             product=product, present_in_basket=True,
                                                             status_of_order='new',
                                                             weight_or_pcs=weight_or_pcs)
                            new_order.save()
                    else:
                        new_order = Order.objects.create(session_key=session_key, client=client,
                                                        product=product, present_in_basket=True, status_of_order='new',
                                                        weight_or_pcs=weight_or_pcs)
                        new_order.save()

                if product.unit == 'ps':
                    if weight_or_pcs:
                        measurement = int(round(weight_or_pcs))
                        weight_or_pcs = measurement

                    new_order, created = Order.objects.get_or_create(session_key=session_key, client=client,
                                                                     product=product, status_of_order='new', present_in_basket=True,
                                                                     defaults={"weight_or_pcs": weight_or_pcs})
                    if not created:
                        if change_weight_or_pcs_order:
                            new_order, created = Order.objects.update_or_create(session_key=session_key, client=client,
                                                                                product=product, present_in_basket=True,
                                                                                status_of_order='new',
                                                                                defaults={
                                                                                    "weight_or_pcs": weight_or_pcs})
                        else:
                            new_order.weight_or_pcs += weight_or_pcs
                        new_order.save()
                    else:
                        new_order.save()
            if do_remove:
                Order.objects.filter(id=order_delete_id, client=client, present_in_basket=True, status_of_order='new',
                                     session_key=session_key).update(present_in_basket=False)
                time_threshold = timezone.now() - timedelta(days=365)
                delete_orders = Order.objects.filter(dates_order__lt=time_threshold)
                if delete_orders:
                    delete_orders.delete()
            sums_order = []
            return_dict = dict()
            product_in_basket = Order.objects.filter(client=client, present_in_basket=True, status_of_order='new',
                    session_key=session_key,  product__category_plus_type_product__category__is_staff=False).order_by('dates_order')
            count_orders_in_basket = product_in_basket.count()
            return_dict['count_orders_in_basket'] = count_orders_in_basket
            return_dict['orders'] = list()

            for item in product_in_basket:
                product_dict = dict()
                product_dict['id'] = item.id
                product_dict['product_id'] = item.product.id
                product_dict['weight_or_pcs'] = item.weight_or_pcs
                product_dict['price_per_item'] = item.product.price
                product_dict['unit'] = item.product.get_unit_display()
                photo = Photo.objects.filter(is_active=True, main_photo=True, product_id=item.product.id).first()
                if photo:
                    product_dict['photo'] = photo.photo.url
                else:
                    product_dict['photo'] = ''
                product_dict['discount_total'] = item.discount_total
                product_dict['category_plus_type'] = item.product.category_plus_type_product.category_plus_type
                product_dict['product_name'] = item.product.name
                product_dict['slug_product'] = item.product.slug_product
                product_dict['absolute_slug_product'] = item.product.get_absolute_url()
                sum_one = item.weight_or_pcs * (item.product.price - (item.product.price/100 * item.discount_total))
                product_dict['sum_one'] = round(sum_one, 2)
                sums_order.append(sum_one)
                return_dict['orders'].append(product_dict)
            return_dict['total_amount'] = round(sum(sums_order), 2)
            return JsonResponse(return_dict)

