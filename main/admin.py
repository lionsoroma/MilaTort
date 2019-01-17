from django.contrib import admin
from orders.models import Order
from django.contrib.auth.admin import User
from .models import *


class ProductClientInline(admin.TabularInline):
    model = Order
    extra = 0
    exclude = ['session_key']


class ClientAdmin (admin.ModelAdmin):

    def user_email(self, instance):
        return instance.user.email

    list_display = ["id", "real_name", "user", "user_email", "phone", "discount_client", "dates_reg"]
    list_editable = ["discount_client"]
    search_fields = ["id", "real_name", "phone", "dates_reg"]
    list_filter = ["dates_reg"]
    inlines = [ProductClientInline]


class Meta:
    model = Client
    admin.site.register(Client, ClientAdmin)


class AddressesAdmin (admin.ModelAdmin):

    list_display = ["id", "town", "street", "building", "apartment"]
    list_editable = ["street", "town", "building", "apartment"]
    search_fields = ["street", "town", "building", "apartment"]


class Meta:
    model = Addresses


admin.site.register(Addresses, AddressesAdmin)


class StreetsAdmin (admin.ModelAdmin):

    list_display = ["id", "city", "name_of_street"]
    list_editable = ["city", "name_of_street"]
    search_fields = ["city", "name_of_street"]


class Meta:
    model = Streets


admin.site.register(Streets, StreetsAdmin)


class CitiesAdmin (admin.ModelAdmin):

    list_display = ["id", "name_of_city"]
    list_editable = ["name_of_city"]
    search_fields = ["name_of_city"]


class Meta:
    model = Cities


admin.site.register(Cities, CitiesAdmin)
