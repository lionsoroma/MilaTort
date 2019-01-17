from django.contrib import admin
from orders.models import Order
from django.contrib.auth.admin import User
from .models import *


class SystemoptionsAdmin (admin.ModelAdmin):
    list_display = ["id", "email_send", "get_email_pool", "phone_send", "get_phone_pool", "email_from"]
    list_editable = ["email_send",  "phone_send",  "email_from"]


class Meta:
    model = Systemoptions
    admin.site.register(Systemoptions, SystemoptionsAdmin)


class EmailwebserviceAdmin (admin.ModelAdmin):
    list_display = ["id", "email_use_tls", "email_host", "email_port", "email_host_user", "email_host_password", "default_from_email", "default_to_email"]
    list_editable = ["email_use_tls", "email_host", "email_port", "email_host_user", "email_host_password", "default_from_email", "default_to_email"]


class Meta:
    model = Emailwebservice
    admin.site.register(Emailwebservice, EmailwebserviceAdmin)


class EmailstaffAdmin (admin.ModelAdmin):
    list_display = ["id", "email_manager", "user_manager"]
    list_editable = ["email_manager", "user_manager"]


class Meta:
    model = Emailstaff
    admin.site.register(Emailstaff, EmailstaffAdmin)


class PhonestaffAdmin (admin.ModelAdmin):
    list_display = ["id", "phone_manager", "user_manager"]
    list_editable = ["phone_manager", "user_manager"]


class Meta:
    model = Phonestaff
    admin.site.register(Phonestaff, PhonestaffAdmin)
