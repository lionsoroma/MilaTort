from django.db import models
from blogs.models import Comment
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from time import time
from transliterate import translit
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
import os


def gen_slug(s):
    new_slug = translit(slugify(s, allow_unicode=True), 'uk', reversed=True).replace(' ', '_').lower()
    return new_slug + '_' + str(int(time()))


class Category(models.Model):
    category = models.CharField(max_length=25, verbose_name='Категорія продукту', null=False, blank=False,
                                help_text='Категорія продукту. Наприклад: Торти, Фігурки, Зефір і т. д.')
    motto = models.CharField(max_length=48, null=True, verbose_name='Гасло категорії', blank=True,
                          help_text='Гасло категорії, яке відображатиметься на сайті.(Максимальна довжина 48 символів)')
    direction_cat = models.IntegerField(validators=[MaxValueValidator(999),  MinValueValidator(0)], verbose_name='Пріорітет показу', blank=False, null=False,
                                    help_text="Порядок показу категорії: менше значить вище", unique=True)
    accessibility = models.BooleanField(default=True, verbose_name='Доступність', help_text="Виняток: кат: Достаква. Повинна бути не доступна(знята галочка)!!!")
    disclaimer = models.TextField(max_length=256, null=True, blank=True, verbose_name='Текст застереження',
                                  help_text="Застереження для категорії, відображатиметься на сайті, коли активувати")
    disclaimer_is_visible = models.BooleanField(default=False, verbose_name=mark_safe(u'Застереження<br/>показувати/<br/>не показувати'),
                                                help_text="Застереження для категорії, відображатиметься на сайті, коли активувати")
    slug_category = models.SlugField(max_length=128, editable=False, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to='category_photo', null=True, blank=True, verbose_name='Загальне фото для категорії')
    is_staff = models.BooleanField(default=False, verbose_name='Супутня категорія', help_text="Товари з цієї категорії "
                                        "не можно замовити окремо, лише з основними товарами. Проте вони доступні для перегляду")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_category = gen_slug(self.category)
        super().save(*args, **kwargs)

    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="%s" style="width: 120px; height: 60px;" />' % self.photo.url)
        else:
            return 'Фото не знайдено'
    image_tag.short_description = "Фото"

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Type(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Наявність')
    slug_type = models.SlugField(max_length=128, editable=False, blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категорія')
    typeof = models.CharField(max_length=25, null=False, blank=False, verbose_name='Тип продукту',
                              help_text='Тип продукту відносно категорії. Наприклад: Весільний, Дитячий для торта або Банановий, Смородиновий для зефіру.')

    min_quantity = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(1)], blank=True, null=True,
                                         verbose_name='Мінімально можлива кількість до замовлення:', default=1,
                                         help_text="Мінімальна кількість шт чи кг, яку можна замовити. Вказується для типу продуктів в цілому. "
                                                   "Значення по замовчуванню(якщо не вказати): 1")
    step_for_min_quantity = models.FloatField(blank=True, null=True, verbose_name='Крок збільшення/зменшення для кількості', default=0.1,
                                                help_text = "Рекомендації: 0.1 для вагових продуктів та 1 для продуктів, "
                                                "що продаються поштучно. Значення по замовчуванню (якщо не вказати): 0.1")
    direction_type = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(0)],
                                        verbose_name='Пріорітет показу', blank=False, null=False, unique=True,
                                        help_text="Порядок показу типу(загальний: для всіх типів): менше значить вище")
    type_description = models.TextField(max_length=256, null=True, verbose_name='Опис типу', blank=True,
                                        help_text='Опис типу, який відображатиметься на сайті.')
    category_plus_type = models.CharField(max_length=50, null=True, blank=True, editable=False, verbose_name='Категорія+Тип продукту:',
                                        help_text='Генерується автоматично!')

    def __str__(self):
        return self.category_plus_type

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типи"

    def save(self, *args, **kwargs):
        if self.category:
            self.category_plus_type = self.category.category + " " + self.typeof.lower()
        if not self.id:
            self.slug_type = gen_slug(self.category_plus_type)
        super(Type, self).save(*args, **kwargs)


class Product(models.Model):
    units = (('kg', 'кг'), ('ps', 'шт'),)
    is_active = models.BooleanField(default=True, verbose_name='Наявність')
    category_plus_type_product = models.ForeignKey(Type, related_name='all_product_of_type', on_delete=models.SET_NULL,
                                                   null=True, verbose_name='Категорія+Тип')
    name = models.CharField(max_length=128, db_index=True, null=True, blank=True, verbose_name='Назва',
                            help_text='Символи "+" будуть замінені на "-"!')
    unit = models.CharField(max_length=2, choices=units, default='kg', verbose_name='КГ/ШТ')
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text='Вартість за кг. чи за шт.',
                                verbose_name='Ціна за одиницю чи за кг.')
    discount_product = models.IntegerField(default=0, validators=[MaxValueValidator(50), MinValueValidator(0)],
                                           help_text='Увага: знижка на продукт сумується зі знижкою клієнта. Можливі значення: 0 - 50',
                                           verbose_name='Знижка на продукт, %')
    product_description = models.TextField(max_length=512, null=True, blank=True, help_text="Опис продукту, який відображатиметься на сайті. Макс.: 512 символів.", verbose_name='Опис продукту')
    slug_product = models.SlugField(max_length=128, editable=False, blank=True, null=True, unique=True)
    comments = models.ManyToManyField(Comment, related_name='commits_from_product', verbose_name='Коментарі / відгуки',
                                      blank=True)
    dates_add = models.DateTimeField(null=True, blank=True, auto_now_add=True, auto_now=False, verbose_name='Дата додання')
    dates_renovation = models.DateTimeField(null=True, blank=True, auto_now_add=False, auto_now=True,
                                            verbose_name='Дата останьої редакції')
    average_rating = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10), MinValueValidator(0)],
                                           help_text='Рейтинг продукту: відображається зірочками, вираховується автоматично на основі оцінки у відгуках',
                                           verbose_name='Рейтинг продукту')
    cooking_time = models.DurationField(null=True, blank=True, help_text='Час виготовлення. '
                                                                     'Величина приблизна і використовується для розрахунку '
                                                                     'терміну приблизного виконання замовлення (відображаються лише години !!!)',
                                           verbose_name='Час виготовлення')

    def __str__(self):
        return '{}{}{}'.format(self.name, ' ', self.category_plus_type_product)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def save(self, *args, **kwargs):
        if self.name:
            while "+" in self.name:
                self.name = self.name.replace("+", "-", 1)
            if " " not in self.name:
                if self.price in range(0, 1000):
                    self.name = self.name[0:15] + ' ' + self.name[15:]
                if self.price in range(1000, 10000):
                    self.name = self.name[0:14]+' '+self.name[14:]
                if self.price > 10000:
                    self.name = self.name[0:13]+' '+self.name[13:]
        if not self.id:
            self.slug_product = gen_slug(self.name)
        super().save(*args, **kwargs)

    def get_new_arrival(self):
        if self.dates_add > timezone.now() - timedelta(days=30):
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('details_product', kwargs={'slug': self.slug_product})


class Photo(models.Model):
    product = models.ForeignKey(Product, blank=True, default=None, on_delete=models.SET_NULL, null=True, verbose_name='Назва продукту')
    photo = models.ImageField(upload_to='products_photo', null=True, verbose_name='Фото продукту', help_text="Прийаються файли(фото) лише у фораматі JPEG!")
    is_active = models.BooleanField(default=True, verbose_name='Доступність', help_text="Дозволяє/забороняє використовувати це фото на сайті в різних розділах")
    land_photo = models.BooleanField(default=True, verbose_name='Стартове', help_text="Центральне фото, яке показується зразу після загрузки. Вимоги: співвідношення сторін 16:9, інакше зображення буде обрізано!")
    blog_photo = models.BooleanField(default=True, verbose_name='Блог', help_text="Фото для розділу блог. Вимоги: співвідношення сторін 16:10, інакше зображення буде обрізано!")
    main_photo = models.BooleanField(default=True, verbose_name='Головне/каталожне', help_text="Головне фото, яке відображається в каталогах. Вимоги: співвідношення сторін 2:3, інакше зображення буде обрізано!")
    dates_upload = models.DateTimeField(null=True, blank=True, auto_now_add=True, auto_now=False, verbose_name='Дата загрузки')
    dates_upgrade = models.DateTimeField(null=True, blank=True, auto_now_add=False, auto_now=True, verbose_name='Дата останьої редакції')

    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="%s" style="width: 60px; height: 60px;" />' % self.photo.url)
        else:
            return 'Фото не знайдено'
    image_tag.short_description = "Фото"

    def __str__(self):
        return '{}'.format(self.photo)

    @property
    def image_filename(self):
        return os.path.basename(self.photo.name)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

