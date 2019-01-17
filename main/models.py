from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
"""
User._meta.get_field('email')._unique = True
"""


class Cities(models.Model):
    name_of_city = models.CharField(max_length=128, null=True, blank=True, db_index=True,
                            help_text="Якщо не вказувати, по замовчуванню: це місто",
                            verbose_name='Назва міста', default='Тернопіль')

    def __str__(self):
        return self.name_of_city

    class Meta:
        verbose_name = "Місто"
        verbose_name_plural = "Міста"


class Streets(models.Model):
    city = models.ForeignKey(Cities, db_index=True, null=False, blank=False, on_delete=models.CASCADE, help_text="Якщо не вказувати, по замовчуванню: це місто",
                            verbose_name='Місто')
    name_of_street = models.CharField(max_length=128, null=False, blank=False, db_index=True, help_text="Назва вулиці",
                                 verbose_name='Вулиця')

    def __str__(self):
        return self.name_of_street

    class Meta:
        verbose_name = "Вулиця"
        verbose_name_plural = "Вулиці"


class Addresses(models.Model):

    town = models.ForeignKey(Cities, db_index=True, null=False, blank=False, on_delete=models.CASCADE, help_text="Якщо не вказувати, по замовчуванню: це місто",
                            verbose_name='Місто')
    street = models.ForeignKey(Streets, db_index=True, null=False, blank=False, on_delete=models.CASCADE, max_length=128, help_text="Назва вулиці",
                                 verbose_name='Вулиця')
    building = models.CharField(max_length=6, null=True, blank=True, db_index=True, help_text="Номер будинку",
                                 verbose_name='Будинок')
    apartment = models.CharField(max_length=6, null=True, blank=True, db_index=True, help_text="Номер квартири (якщо є)",
                                verbose_name='Квартира')

    def __str__(self):
        return '{}{}{}{}{}'.format(self.street, ' ', self.building, '/', self.apartment)

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адреси"


class Client(models.Model):
    user = models.OneToOneField(User, db_index=True, null=False, blank=False, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=128, db_index=True, null=True, blank=True, help_text="Як до Вас звертатись(Імя, Фамілія)",
                                 verbose_name='Реальне імя')
    photo = models.ImageField(upload_to='client_photo', null=True, blank=True, verbose_name='Фото')
    phone = models.CharField(max_length=28, db_index=True, null=True, blank=True, help_text="Номер телефону", unique=True,
                             verbose_name='Номер телефону')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата народження', help_text="Дата народження")
    discount_client = models.IntegerField(default=0, null=True, blank=True, validators=[MaxValueValidator(50),
                                                                                        MinValueValidator(0)],
                                           help_text='Увага: персональна знижка сумується зі знижкою продукту. Можливі значення: 0 - 50',
                                           verbose_name='Персональна знижка, %')
    dates_reg = models.DateTimeField(null=True, db_index=True, blank=True, auto_now_add=True, verbose_name='Дата реєстрації')
    address = models.ForeignKey(Addresses, blank=True, null=True, db_index=True, on_delete=models.SET_NULL,
                                verbose_name='Адреса', help_text="Адреса доставки/проживання")

    def __str__(self):
        return self.real_name

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"

    @receiver(post_save, sender=User)
    def create_user_client(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_client(sender, instance, **kwargs):
        instance.client.save()




