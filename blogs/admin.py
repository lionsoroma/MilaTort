from django.contrib import admin
from .models import *
from django.forms import Textarea


class CommentAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={
                'rows': 3,
                'cols': 50,
                'style': 'height: 3.5em;'})}}

    list_display = ["id", "client_commit", "rating", "product_commit", "r_commit", "dates_commit"]
    search_fields = ["id", "client_commit", "product_commit", "r_commit", "dates_commit"]
    list_filter = ["dates_commit"]


class Meta:
    model = Comment


admin.site.register(Comment, CommentAdmin)
