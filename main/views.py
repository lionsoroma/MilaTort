from django.shortcuts import render
from .forms import ClientForm
from orders.models import Order
from products.models import Photo
from products.models import Type
from products.models import Category
from products.models import Product
from systemoptions.models import Systemoptions
from blogs.models import Comment
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from main.smsc_api import *
from transliterate import translit
import random


def generate_username(first_name, last_name):
    val = "{0}{1}".format(first_name[0], last_name).lower()
    x=0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}".format(val, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 1000000:
            raise Exception("Name is super popular!")


def get_real_name(username):
    lst = username.split()
    last_name = lst[-1]
    first_name = lst[0]
    if not last_name:
        first_name = last_name
    full_name = dict()
    full_name['last_name'] = last_name
    full_name['first_name'] = first_name
    return full_name


class BlogOfRecord:
    def __init__(self, photo, comment, count):
        self.photo = photo
        self.comment = comment
        self.count = count

    def edit_key(self):
        last = abs(self.count) % 100
        if last in range(10, 20):
            key_new = 'ів'
        else:
            last = abs(last) % 10
            key_new = {
                last == 0: 'ів',
                last == 1: '',
                last > 1: 'і',
                last > 4: 'ів',
            }[True]
        full_key = 'Коментар'+key_new
        return full_key


def main(request):
    blogs = []
    land_photos = Photo.objects.filter(land_photo=True, is_active=True).order_by('?')[:15]
    temp_blogs = Photo.objects.filter(blog_photo=True, is_active=True).order_by('dates_upload')
    for any_photo in temp_blogs:
        required_entries = Comment.objects.filter(product_commit_id=any_photo.product_id, r_commit__isnull=False).exclude(r_commit='')
        if required_entries:
            blogs.append(BlogOfRecord(any_photo,
                                      required_entries.last(),
                                      required_entries.count()))

    random.shuffle(blogs)
    blogs = blogs[:3]
    categories = Category.objects.filter(accessibility=True).order_by('direction_cat')
    types = Type.objects.filter(is_active=True).order_by('direction_type')
    products = Product.objects.filter(price__exact=True)
    min_prices_counts_units = []
    for any_type in types:
        temporary = Product.objects.filter(category_plus_type_product_id=any_type.id, is_active=True).order_by('price')
        if temporary:
            min_prices_counts_units.append({'min_price_of_this_type': temporary.first().price, 'count_of_this_type':
                temporary.count(), 'unit_of_this_type': temporary.first().get_unit_display()})
        else:
            min_prices_counts_units.append(None)
    if request.method == 'POST':
        submitter = request.POST['submitter']
        username = request.POST['username']
        full_name = get_real_name(username)
        last_name = full_name['last_name']
        first_name = full_name['first_name']
        request.POST = request.POST.copy()
        request.POST['username'] = generate_username(last_name, first_name)
        client_form = ClientForm(request.POST or None)
        if client_form.is_valid():
            client = client_form.save_user(last_name, first_name)
            if not request.session.session_key:
                request.session.save()
            session_key = request.session.session_key
            quick_order = Order(client=client, order_description=request.POST['order_description'], status_of_order='new',
                                present_in_basket=False, session_key=session_key)
            quick_order.save()
            status_quick = inform_service_quick(quick_order, submitter)
            if status_quick:
                data = {'success': True}
            else:
                data = {'success': False, 'error': 'error'}
    return render(request, 'main/index.html', locals())


def inform_service_quick(quick_order, submitter):
    if quick_order:
        date_of_quick_order = quick_order.dates_order
        quick_order_subj = 'Новий (ШВИДКИЙ) заказ: від ' + date_of_quick_order.strftime('%Y-%m-%d %H:%M')
        w_master_options = Systemoptions.objects.all().first()
        if w_master_options:
            if w_master_options.email_send:
                context = {'quick_order': quick_order}
                if submitter == 'call':
                    context.update({'submitter': submitter})
                config_quick = w_master_options.email_from
                to_obj_quick = list(w_master_options.emails_pool.all())
                to_quick = []
                for to_item_quick in to_obj_quick:
                    to_quick.append(to_item_quick.email_manager)
                backend_quick = EmailBackend(host=config_quick.email_host, port=config_quick.email_port, username=config_quick.email_host_user,
                                       password=config_quick.email_host_password, use_tls=config_quick.email_use_tls)
                html_quick = render_to_string('quick_email_template/quick_email_template.html', context=context).strip()
                msg_quick = EmailMultiAlternatives(subject=quick_order_subj, body=html_quick,
                                                 from_email=w_master_options.email_from.default_from_email,
                                                 to=to_quick, reply_to=['ivanmila24@gmail.com'], connection=backend_quick)
                msg_quick.content_subtype = 'html'
                msg_quick.mixed_subtype = 'related'
                msg_quick.send()
                if w_master_options.phone_send:
                    smsc = SMSC()
                    phone_numbers_quick = w_master_options.phones_pool.all()
                    for phone_number_quick in phone_numbers_quick:
                        phone_quick = '8' + phone_number_quick.phone_manager
                        full_str = translit(quick_order_subj, 'uk', reversed=True) + translit(". № заказу(ID): ", 'uk',
                                                                                         reversed=True) + str(
                            quick_order.id) + translit(". Деталі в поштові скринці чи в БД.", 'uk', reversed=True)
                        r = smsc.send_sms(phone_quick, full_str, sender="MilaTort Team")
                return True
        else:
            return False
    else:
        return False
