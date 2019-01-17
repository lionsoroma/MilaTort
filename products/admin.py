from django.contrib import admin
from .models import *
from django.db.models import Count
from django.forms import Textarea
from django.forms import TextInput


class ProductPhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


class ProductAdmin (admin.ModelAdmin):
    self_id = None

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={
                'rows': 4,
                'cols': 60,
                'style': 'height: 4.5em;'})}}

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.self_id = obj.id
        return super(ProductAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "comments":
            kwargs['queryset'] = Comment.objects.filter(product_commit_id=self.self_id)
        return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        return Product.objects.annotate(count_of_photos=Count('photo'))

    def count_of_photos(self, obj):
        return obj.count_of_photos

    count_of_photos.admin_order_field = "count_of_photos"
    count_of_photos.short_description = "Кількість фото"
    list_display = ["name", "category_plus_type_product", "unit", "price", "discount_product", "is_active", "count_of_photos", "dates_add", "dates_renovation"]
    list_editable = ["category_plus_type_product", "unit", "price", "discount_product", "is_active"]
    search_fields = ["name", "category_plus_type_product__category_plus_type", "price"]
    inlines = [ProductPhotoInline]


class Meta:
    model = Product
    admin.site.register(Product, ProductAdmin)


class PhotoAdmin (admin.ModelAdmin):
    list_display = ["id", "product", "is_active", "image_tag", "land_photo", "blog_photo", "main_photo", "dates_upload", "dates_upgrade"]
    list_editable = ["is_active", "land_photo", "blog_photo", "main_photo"]
    list_filter = ["dates_upload", "dates_upgrade"]


class Meta:
    model = Photo
    admin.site.register(Photo, PhotoAdmin)


class TypeAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={
                'rows': 2,
                'cols': 35,
                'style': 'height: 2.5em;'})}}

    list_display = ["id", "typeof", "category", "category_plus_type", "type_description", "is_active", "direction_type"]
    list_editable = ["typeof", "category", "type_description", "is_active", "direction_type"]


class Meta:
    model = Type
    admin.site.register(Type, TypeAdmin)


class CategoryAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '16'})},
    }

    list_display = ["id", "accessibility", "category", "motto", "is_staff", "direction_cat", "disclaimer_is_visible", "image_tag"]
    search_fields = ["category", "motto"]
    list_editable = ["accessibility", "category", "motto", "is_staff", "direction_cat", "disclaimer_is_visible"]


class Meta:
    model = Category
    admin.site.register(Category, CategoryAdmin)


