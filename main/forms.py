from django import forms
from django.contrib.auth.models import User
from orders.models import Order
from main.models import Client
import random
import string


def generate_pw():
    length = random.randint(6, 20) - 8
    pwd = []
    pwd.append(random.choice(string.ascii_lowercase))
    pwd.append(random.choice(string.ascii_uppercase))
    pwd.append(str(random.randint(0, 9)))
    random.shuffle(pwd)
    return ''.join(pwd)


class ClientForm(forms.ModelForm):
    phone = forms.CharField(max_length=28)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save_user(self, last_name, first_name):
        username = self.cleaned_data['username']
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email']
        try:
            new_client = Client.objects.get(phone=phone)
        except Client.DoesNotExist:
            new_user = User.objects.create(username=username, last_name=last_name, first_name=first_name,
                                           email=email)
            new_user.client.phone = phone
            new_user.set_password(generate_pw())
            new_user.client.real_name = last_name + ' ' + first_name
            new_user.save()
        else:
            return new_client
        return new_user.client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = [""]