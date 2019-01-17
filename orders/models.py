from django.db import models
from products.models import Product
from main.models import Client
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

units_of_status = (('new', 'новий'), ('executed', 'виконаний'))


class Status(models.Model):
    current = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.current

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статуси"


class Order(models.Model):
    client = models.ForeignKey(Client, db_index=True, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Клієнт')
    product = models.ForeignKey(Product, db_index=True, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    order_description = models.TextField(max_length=128, null=True, blank=True, help_text="Опис заказу",
                                         verbose_name='Опис заказу')
    weight_or_pcs = models.DecimalField(max_digits=5, blank=True, decimal_places=1, default=1,
                                        validators=[MinValueValidator(1)], help_text='Бажана вага чи кількість шт.',
                                        verbose_name='Вага чи кількість')
    unitof = models.CharField(max_length=2, blank=True, choices=Product.units, default='kg', verbose_name='КГ/ШТ')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True,
                                         verbose_name='Ціна за од.',
                                         help_text="Якщо не вводити в це поле жодних даних, то цінна підтягнеться з БД ")
    discount_total = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(100), MinValueValidator(0)],
                                         verbose_name='Суми знижок, %', editable=False)
    total_price = models.DecimalField(max_digits=10, blank=True, decimal_places=2, default=0, editable=False,
                                      verbose_name='Сума зі знижками')
    dates_order = models.DateTimeField(null=True, db_index=True, blank=True, auto_now_add=True, auto_now=False,
                                       verbose_name='Дата оформлення')
    update_order = models.DateTimeField(null=True, db_index=True, blank=True, auto_now_add=False, auto_now=True)
    session_key = models.CharField(max_length=128, db_index=True, null=True, blank=True, default=None,
                                   verbose_name='Ключ сесії(служова інформація)')
    present_in_basket = models.BooleanField(null=True, blank=True, default=True, verbose_name="Присутність в корзині",
                                            help_text="Заказ зберігаєть в списку заказів навіть тоді, коли клієнт його видалив."
                                                      "Використовується для статистики. В кошик він не попадає!",)
    status_of_order = models.CharField(max_length=10, blank=False, null=False, choices=units_of_status, default='new', verbose_name='Статус заказу')
    is_stuffing_id = models.IntegerField(null=True, blank=True, verbose_name='Начинка/серединка, якщо є',
                                            help_text='Службове поле.')

    def __str__(self):
        return '{} {} {}'.format(self.product, self.weight_or_pcs, self.unitof)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Закази"

    def save(self, *args, **kwargs):
        if self.product:
            if self.weight_or_pcs:
                if self.product.unit == 'ps':
                    measurement = int(round(self.weight_or_pcs))
                    self.weight_or_pcs = measurement
            self.unitof = self.product.unit
            if self.client:
                self.discount_total = self.client.discount_client + self.product.discount_product
            else:
                self.discount_total = self.product.discount_product
            if self.price_per_item != self.product.price and self.price_per_item != 0:
                price_per_item = self.price_per_item
            else:
                price_per_item = self.product.price
            self.price_per_item = price_per_item
            self.total_price = self.weight_or_pcs * price_per_item
            self.total_price = self.total_price - ((self.total_price /100) * self.discount_total)
        super(Order, self).save(*args, **kwargs)


class Basket(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False, verbose_name='Вартість кошика',help_text="Всі знижки враховані")
    client = models.ForeignKey(Client, related_name='basket_of_client', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Клієнт')
    orders = models.ManyToManyField(Order, related_name='orders_in_basket', blank=False, verbose_name='Закази в кошику')
    notes = models.TextField(max_length=256, null=True, blank=True, help_text="Побажання до заказу", verbose_name='Нотатки для кошика')
    date_of_readiness = models.DateTimeField(null=False, blank=False, verbose_name="Готовність на(дата):", help_text="На коли має бути готоаий заказ: дата і час", default=timezone.now)
    delivery_required = models.BooleanField(null=True, blank=True, default=False, verbose_name="Потібна доставка?", help_text="Саму доставку потрібно вибирати як окремий продукт",)
    dates_basket = models.DateTimeField(null=True, blank=False, auto_now=False, auto_now_add=True,
                                       verbose_name='Дата оформлення')
    update_basket = models.DateTimeField(null=True, blank=True, auto_now_add=False, auto_now=True)
    state_of_status = models.CharField(max_length=10, blank=False, null=False, choices=units_of_status, default='new', verbose_name='Статус кошика')
    session_key = models.CharField(max_length=128, db_index=True, null=True, blank=True, default=None,
                                   verbose_name='Ключ сесії(служова інформація)')

    def __str__(self):
        return '{} {}'.format(self.client.real_name, self.total_amount)

    def get_order(self):
        return ",\n".join([str(o) for o in self.orders.all()])

    get_order.short_description = 'Товари в кошику'

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"
