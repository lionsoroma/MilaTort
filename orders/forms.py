from django import forms
from orders.models import Order


class OrderListForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["product", "weight_or_pcs", "session_key"]