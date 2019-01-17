from django import forms
from main.models import Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class RegisterForm(UserChangeForm):
    phone = forms.CharField(max_length=28)
    real_name = forms.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean_username(self):
        data = self.cleaned_data['username']
        duplicate_users = User.objects.filter(username=data)
        if self.instance.pk is not None:
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError('Такий логін вже зайнятий! Придумайте щось інше!')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        leave = User.objects.filter(email=data)
        if leave.exists():
            test_false = leave.filter(email__exact='')
            if test_false.exists():
                return data
            else:
                raise forms.ValidationError(
                    'Такий Email вже використовується! Якщо це Ваш Email адрес спробуйте відновити свій обліковий запис!')
        else:
            return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if User.objects.filter(client__phone=data).exists():
            raise forms.ValidationError('Такий номер телефону вже використовується! Якщо це Ваш номер телефону спробуйте відновити свій обліковий запис!')
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) <= 2:
            raise forms.ValidationError('Пароль повинен містити хоча б два символи, будь-ласка!')
        return data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User


class ResetTelForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['phone']






