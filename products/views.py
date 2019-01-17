from django.shortcuts import render
from .models import Product
from orders.models import Order
from .forms import RegisterForm
from .forms import LoginForm
from .forms import ResetTelForm
from products.models import Type
from products.models import Photo
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import login, logout
from django.db.models import F
from main.smsc_api import *
from main.forms import generate_pw
from transliterate import translit
import random
import json
from django.views.decorators.cache import cache_control


def get_hide_username(username, percent_hide):
    guessed_string = username
    len_part_hide = round((len(username) / 100) * percent_hide)
    used_letters = []
    random.seed(version=2)
    for i in range(0, len_part_hide):
        hide_pos = random.randint(1, len(username) - 1)
        if hide_pos not in used_letters:
            used_letters.append(hide_pos)
            guessed_string = guessed_string[:hide_pos] + '*' + guessed_string[hide_pos + 1:]
    ''.join(guessed_string)
    return guessed_string


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def login_logout(request):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        if len(request.POST.dict()) == 0:
            if request.user.is_active:
                Order.objects.filter(client=request.user.client, present_in_basket=True, session_key=session_key).update(
                    client=None, discount_total=F('discount_total')-request.user.client.discount_client)
                old_session_key = session_key
                logout(request)
                if not request.session.session_key:
                    request.session.save()
                session_key = request.session.session_key
                Order.objects.filter(client=None, present_in_basket=True,
                                     session_key=old_session_key).update(session_key=session_key)
                data = {'success': True}
            else:
                data = {'success': False, 'error': 'Сам не знаю, що за помилка!'}
            return HttpResponse(json.dumps(data), content_type="application/json")
        if len(request.POST.dict()) <= 3:
            login_form = LoginForm(request.POST or None)
            if login_form.is_valid():
                data = {}
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        Order.objects.filter(client=None, present_in_basket=True, session_key=session_key).update(client=user.client,
                                                                                                                  discount_total=F('discount_total')+user.client.discount_client)
                        data = {'success': True}
                else:
                    data = {'success': False, 'error': 'Провірте правильність паролю чи логіну'}
            else:
                data = {'success': False, 'error': 'Користувач не активний або відсутній'}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            if len(request.POST.dict()) > 3:
                register_form = RegisterForm(request.POST or None)
                if register_form.is_valid():
                    username = register_form.cleaned_data['username']
                    real_name = register_form.cleaned_data['real_name']
                    password = register_form.cleaned_data['password']
                    if real_name:
                        lst = real_name.split()
                        last_name = lst[-1]
                        first_name = lst[0]
                    else:
                        first_name = username
                        last_name = username
                    email = register_form.cleaned_data['email']
                    phone = register_form.cleaned_data['phone']
                    new_user = User.objects.create_user(email=email, username=username,
                                                            first_name=first_name, last_name=last_name, is_active=True)
                    new_user.client.real_name = real_name
                    new_user.client.phone = phone
                    new_user.set_password(password)
                    new_user.save()
                    return JsonResponse(register_form.cleaned_data)
                else:
                    return JsonResponse(register_form.errors)


def password_reset_via_tel(request):
    if request.method == 'POST':
        reset_tel_form = ResetTelForm(request.POST or None)
        if reset_tel_form.is_valid():
            phone = reset_tel_form.cleaned_data['phone']
            if phone:
                password_reset = generate_pw() + generate_pw()
                try:
                    user = User.objects.get(client__phone=phone)
                except User.DoesNotExist:
                    return render(request, 'password_reset/password_reset_via_tel_confirm.html', locals()) #no_user
                else:
                    smsc = SMSC()
                    phone_number = '8'+phone
                    login_shadow = get_hide_username(user.username, 50)
                    full_str = translit("Для Вашого логіна ", 'uk', reversed=True)+login_shadow+translit(" парол було успішно змінено. Новий парол: ", 'uk', reversed=True)+password_reset
                    r = smsc.send_sms(phone_number, full_str, sender="MilaTort Team")
                    user.set_password(password_reset)
                    user.is_active = False
                    user.save()
                    return render(request, 'password_reset/password_reset_via_tel_done.html', context={'phone': phone_number})
            else:
                return render(request, 'password_reset/password_reset_via_tel_confirm.html', locals())
        return render(request, 'password_reset/password_reset_via_tel_confirm.html', locals())


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def list_product(request, slug):
    photos_of_product = []
    list_of_types = Type.objects.get(slug_type__iexact=slug)
    category_for_back = list_of_types.category.slug_category
    product_of_type = Product.objects.filter(category_plus_type_product_id=list_of_types.id, is_active=True).order_by('category_plus_type_product__category__direction_cat')
    for this_product in product_of_type:
        photos_of_product.append(Photo.objects.filter(product_id=this_product.id, is_active=True, main_photo=True).first())
    request.session['referer_path'] = request.build_absolute_uri()
    return render(request, 'list_product/list_product.html', context={'product_of_type': product_of_type,
                                                                      'title_of_type': list_of_types,
                                                                      'photos_of_product': photos_of_product,
                                                                      'category_for_back': category_for_back})

