from django.contrib import admin
from .models import *
from django.forms import TextInput
from django.forms import Textarea


class OrderAdmin (admin.ModelAdmin):
    exclude = ['session_key']

    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'size': '7'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '7'})}
    }

    list_display = ["id", "client", "present_in_basket", "status_of_order", "product", "order_description", "weight_or_pcs", "price_per_item", "discount_total", "total_price", "dates_order"]
    list_editable = ["present_in_basket", "status_of_order", "weight_or_pcs", "price_per_item"]
    search_fields = ["id", "client", "product", "dates_order"]


class Meta:
    model = Order


admin.site.register(Order, OrderAdmin)


class BasketAdmin (admin.ModelAdmin):
    exclude = ['session_key']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={
                'rows': 3,
                'cols': 30,
                'style': 'height: 3.5em;'})}}

    list_display = ["id", "get_order", "total_amount", "state_of_status", "client", "notes", "dates_basket", "date_of_readiness", "delivery_required"]
    list_editable = ["notes", "state_of_status", "date_of_readiness", "delivery_required"]
    search_fields = ["total_amount", "client", "notes", "dates_basket", "date_of_readiness", "delivery_required"]


class Meta:
    model = Basket


admin.site.register(Basket, BasketAdmin)