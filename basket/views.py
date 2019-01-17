from django.shortcuts import render
from django.db.models import Min, Max
from products.models import Product, Photo
from orders.models import Basket
from orders.models import Order
from main.models import Cities
from main.models import Streets
from main.models import Addresses
from orders.views import convert_trueTrue_falseFalse
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.timezone import make_aware
from systemoptions.models import Systemoptions
from django.core.mail.backends.smtp import EmailBackend
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from PIL import Image
from io import BytesIO
from django.http.response import JsonResponse
from transliterate import translit
import json
from main.smsc_api import *
from django.utils import timezone
from pathlib import Path
from django.views.decorators.cache import cache_control


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def basket_finish(request):
    client = None
    if request.user.is_active:
        client = request.user.client
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    if request.method == 'POST':
        to_remove = convert_trueTrue_falseFalse(request.POST.get('to_remove'))
        super_order_id = request.POST.get('super_order_id')
        super_weight_or_pcs = request.POST.get('super_weight_or_pcs')
        super_stuff_id = request.POST.get('stuff_id')
        if to_remove:
            Order.objects.filter(id=super_order_id, client=client, present_in_basket=True, product__category_plus_type_product__category__is_staff=False,
                                 session_key=session_key, status_of_order='new').update(present_in_basket=False)
        if not to_remove:
            Order.objects.filter(id=super_order_id, client=client, present_in_basket=True, product__category_plus_type_product__category__is_staff=False,
                                 session_key=session_key, status_of_order='new').update(weight_or_pcs=super_weight_or_pcs)
            if super_stuff_id:
                super_type_stuff = Product.objects.get(id=super_stuff_id,
                                                       category_plus_type_product__category__is_staff=True).category_plus_type_product.typeof
                super_name_of_type_stuff = Product.objects.get(id=super_stuff_id,
                                                               category_plus_type_product__category__is_staff=True).name
                super_description = 'Начинка/серединка - ' + super_type_stuff + ': ' + super_name_of_type_stuff
                Order.objects.filter(id=super_order_id, client=client, present_in_basket=True, product__category_plus_type_product__category__is_staff=False,
                                     session_key=session_key, status_of_order='new').update(order_description=super_description, is_stuffing_id=super_stuff_id)

    stuffing = Product.objects.filter(category_plus_type_product__category__is_staff=True, category_plus_type_product__category__accessibility=True)
    start_calendar_date = None
    stuff_of_deltas = []
    full_stuff_prices_with_discount = []
    for stuff_in in stuffing:
        stuff_delta_s = None
        if stuff_in.cooking_time:
            stuff_delta = stuff_in.cooking_time
            stuff_delta_s = stuff_delta.seconds
        stuff_of_deltas.append(stuff_delta_s)
        price_stuff_in = stuff_in.price
        discount_stuff_in = stuff_in.discount_product
        if client:
            discount_stuff_in = discount_stuff_in + client.discount_client
        price_stuff_in = price_stuff_in - ((price_stuff_in / 100) * discount_stuff_in)
        full_stuff_prices_with_discount.append(price_stuff_in)

    super_orders = Order.objects.filter(client=client, present_in_basket=True, product__category_plus_type_product__category__is_staff=False,
                                 session_key=session_key, status_of_order='new').order_by('dates_order')
    with_hours = super_orders.filter(product__cooking_time__isnull=False)
    if with_hours:
        hours_total = with_hours.aggregate(res=Sum(F('product__cooking_time')))
        start_calendar_date = datetime.now() + hours_total['res']
    stuff_prices_with_discount = []
    order_prices_with_discount = []
    stuff_cooking_time_array = []
    stuff_hours_total_s = timedelta(0)
    time_of_deltas = []
    item_row_sums = []
    for super_order in super_orders:
        time_delta_s = None
        if super_order.product.cooking_time:
            time_delta = super_order.product.cooking_time
            time_delta_s = time_delta.seconds
        time_of_deltas.append(time_delta_s)
        stuff_tmp = None
        stuff_cooking_time = None
        ss_time_delta = None
        if super_order.is_stuffing_id:
            stuff = Product.objects.get(id=super_order.is_stuffing_id, category_plus_type_product__category__is_staff=True,
                                        category_plus_type_product__category__accessibility=True)
            stuff_price = stuff.price
            stuff_discount = stuff.discount_product
            if stuff.cooking_time:
                stuff_cooking_time = stuff.cooking_time
                ss_time_delta = stuff_cooking_time.seconds
                stuff_hours_total_s = stuff_hours_total_s + stuff_cooking_time
            if client:
                stuff_discount = stuff_discount + client.discount_client
            stuff_tmp = stuff_price - ((stuff_price / 100) * stuff_discount)
        super_discount = super_order.product.discount_product
        if client:
            super_discount = super_discount + client.discount_client
        order_tmp = super_order.product.price - ((super_order.product.price / 100) * super_discount)
        order_prices_with_discount.append(order_tmp)
        stuff_prices_with_discount.append(stuff_tmp)
        stuff_cooking_time_array.append(ss_time_delta)
        sum_tmp = order_tmp
        if stuff_tmp:
            sum_tmp = sum_tmp + stuff_tmp
        item_sum_tmp = sum_tmp * super_order.weight_or_pcs
        item_row_sums.append(item_sum_tmp)
        total_sum_basket = sum(item_row_sums)
        if stuff_hours_total_s and start_calendar_date:
            start_calendar_date = start_calendar_date + stuff_hours_total_s
        max_price = Product.objects.filter(category_plus_type_product__category__is_staff=True,
                                           category_plus_type_product__category__accessibility=False, ).aggregate(Max('price'))['price__max']
        delivery_price_max_with_discount = max_price
        discount_base_max_delivery = 0
        total_discount_delivery_max = 0
        delivery_price_max = Product.objects.filter(price=max_price).first()
        if delivery_price_max.discount_product:
            discount_base_max_delivery = delivery_price_max.discount_product
        if client:
            total_discount_delivery_max = discount_base_max_delivery + client.discount_client
        delivery_price_max_with_discount = max_price - ((max_price / 100) * total_discount_delivery_max)
        min_price = Product.objects.filter(category_plus_type_product__category__is_staff=True,
                                           category_plus_type_product__category__accessibility=False).aggregate(Min('price'))['price__min']
        delivery_price_min_with_discount = min_price
        discount_base_min_delivery = 0
        total_discount_delivery_min = 0
        delivery_price_min = Product.objects.filter(price=min_price).first()
        if delivery_price_min.discount_product:
            discount_base_min_delivery = delivery_price_min.discount_product
        if client:
            total_discount_delivery_min = discount_base_min_delivery + client.discount_client
        delivery_price_min_with_discount = min_price - ((min_price / 100) * total_discount_delivery_min)
    return render(request, 'basket_finish/basket_finish.html', locals())


def cities_streets(request):
    if request.method == 'POST':
        cities = Cities.objects.all()
        streets = Streets.objects.all()
        return_dict = dict()
        city_or_street = request.POST.get('city_or_street')
        if city_or_street == 'city':
            return_dict['cities'] = list()
            for city in cities:
                city_dict = dict()
                city_dict['id'] = city.id
                city_dict['name_of_city'] = city.name_of_city
                return_dict['cities'].append(city_dict)
        if city_or_street == 'street':
            return_dict['streets'] = list()
            for street in streets:
                street_dict = dict()
                street_dict['id'] = street.city.id
                street_dict['name_of_street'] = street.name_of_street
                return_dict['streets'].append(street_dict)
        return JsonResponse(return_dict)


def inform_service(basket_items):
    if basket_items:
        date_of_order = basket_items.dates_basket
        basket_subj = 'Новий заказ: від ' + date_of_order.strftime('%Y-%m-%d %H:%M')
        web_master_options = Systemoptions.objects.all().first()
        if web_master_options:
            if web_master_options.email_send:
                orders_items = basket_items.orders.all()
                context = {'basket_items': basket_items}
                small_photos_in_order = []
                small_photos_in_stuff = []
                small_names_in_stuff = []
                for order_item in orders_items:
                    get_image = Photo.objects.filter(product_id=order_item.product.id, is_active=True,
                                                     main_photo=True).first()
                    if get_image:
                        small_photos_in_order.append(get_image)
                    else:
                        small_photos_in_order.append(None)
                    if order_item.is_stuffing_id:
                            stuff_image = Photo.objects.filter(product_id=order_item.is_stuffing_id).first()
                            small_names_in_stuff.append(Product.objects.get(id=order_item.is_stuffing_id))
                            if stuff_image:
                                small_photos_in_stuff.append(stuff_image)
                            else:
                                small_photos_in_stuff.append(None)
                    else:
                        small_names_in_stuff.append(None)
                context.update({'small_photos_in_order': small_photos_in_order})
                context.update({'small_photos_in_stuff': small_photos_in_stuff})
                context.update({'small_names_in_stuff': small_names_in_stuff})
                config = web_master_options.email_from
                to_obj = list(web_master_options.emails_pool.all())
                to = []
                for to_item in to_obj:
                    to.append(to_item.email_manager)
                backend = EmailBackend(host=config.email_host, port=config.email_port, username=config.email_host_user,
                                       password=config.email_host_password, use_tls=config.email_use_tls)
                html_content = render_to_string('congratulations/congratulations.html', context=context).strip()
                msg = EmailMultiAlternatives(subject=basket_subj, body=html_content, from_email=web_master_options.email_from.default_from_email,
                                             to=to, reply_to=['ivanmila24@gmail.com'], connection=backend)
                msg.content_subtype = 'html'
                msg.mixed_subtype = 'related'
                for order_item in orders_items:
                    get_image = Photo.objects.filter(product_id=order_item.product.id, is_active=True,
                                                     main_photo=True).first()
                    if get_image:
                        crop_image = Image.open(get_image.photo)
                        suffix = Path(get_image.image_filename).suffix
                        if suffix.lower() == '.png':
                            crop_image = crop_image.convert('RGB')
                        (width, height) = 80, 120
                        size = (width, height)
                        crop_image = crop_image.resize(size, Image.ANTIALIAS)
                        mem_buff = BytesIO()
                        crop_image.save(mem_buff, "JPEG")
                        image_mime = MIMEImage(mem_buff.getvalue())
                        mem_buff.close()
                        image_mime.add_header('Content-ID', '<{}>'.format(get_image.image_filename))
                        msg.attach(image_mime)
                    if order_item.is_stuffing_id:
                            stuff_image = Photo.objects.filter(product_id=order_item.is_stuffing_id).first()
                            if stuff_image:
                                stuff_crop_image = Image.open(stuff_image.photo)
                                suffix = Path(stuff_image.image_filename).suffix
                                if suffix.lower() == '.png':
                                    stuff_crop_image = stuff_crop_image.convert('RGB')
                                (width, height) = 80, 120
                                size_stuff = (width, height)
                                stuff_crop_image = stuff_crop_image.resize(size_stuff, Image.ANTIALIAS)
                                mem_buff_stuff = BytesIO()
                                stuff_crop_image.save(mem_buff_stuff, "JPEG")
                                image_mime_stuff = MIMEImage(mem_buff_stuff.getvalue())
                                mem_buff_stuff.close()
                                image_mime_stuff.add_header('Content-ID', '<{}>'.format(stuff_image.image_filename))
                                msg.attach(image_mime_stuff)
                msg.send()
            if web_master_options.phone_send:
                smsc = SMSC()
                phone_numbers = web_master_options.phones_pool.all()
                for phone_number in phone_numbers:
                    phone = '8' + phone_number.phone_manager
                    full_str = translit(basket_subj, 'uk', reversed=True) + translit(". № заказу(ID): ", 'uk', reversed=True) + str(basket_items.id) + translit(". Деталі в поштові скринці чи в БД.", 'uk', reversed=True)
                    r = smsc.send_sms(phone, full_str, sender="MilaTort Team")
            return True
        else:
            return False
    else:
        return False


def basket_table(request):
    if request.method == 'POST':
        city_last = request.POST.get('city_last')
        street_last = request.POST.get('street_last')
        house_last = request.POST.get('house_last')
        apt_last = request.POST.get('apt_last')
        notes_last = request.POST.get('notes_last')
        date_last = int(request.POST.get('date_last'))
        head_total_amount = request.POST.get('head_total_amount')
        date_insert = make_aware(datetime.fromtimestamp((date_last / 1000)))
        new_address = None
        client = None
        if request.user.is_active:
            client = request.user.client
            if city_last and street_last and house_last:
                new_town, created = Cities.objects.get_or_create(name_of_city=city_last)
                new_street, created = Streets.objects.get_or_create(name_of_street=street_last, city=new_town)
                new_address, created = Addresses.objects.get_or_create(town=new_town, street=new_street, building=house_last,
                                                           apartment=apt_last)
                new_address.save()
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        orders_items = Order.objects.filter(client=client, present_in_basket=True, product__category_plus_type_product__category__is_staff=False,
                                     session_key=session_key, status_of_order='new')
        basket_items = Basket.objects.create(session_key=session_key, client=client, state_of_status='new')
        basket_items.date_of_readiness = date_insert
        basket_items.notes = notes_last
        if city_last and street_last and house_last:
            basket_items.delivery_required = True
            if new_address:
                client.address = new_address
                client.save()
        else:
            basket_items.delivery_required = False
        basket_items.total_amount = head_total_amount
        basket_items.save()
        basket_items.orders.set(orders_items)
        status = inform_service(basket_items)
        if status:
            orders_items.update(present_in_basket=False)
            data = {'success': True}
            time_threshold = timezone.now() - timedelta(days=365)
            delete_baskets = Basket.objects.filter(dates_basket__lt=time_threshold)
            if delete_baskets:
                delete_baskets.delete()
        else:
            data = {'success': False, 'error': 'error'}
        return HttpResponse(json.dumps(data), content_type="application/json")
