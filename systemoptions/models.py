from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Emailstaff(models.Model):
    email_manager = models.EmailField(null=False, blank=False, verbose_name='Email менеджера:')
    user_manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Користувач (User) якому належить Email адрес',
                                                                  help_text='Може бути не вказаний!')

    def __str__(self):
        return self.email_manager

    class Meta:
        verbose_name = "Email менеджера"
        verbose_name_plural = "Emails менеджерів"


class Phonestaff(models.Model):
    phone_manager = models.CharField(null=False, blank=False, max_length=10, validators=[RegexValidator(regex='^\d{10}$',
                                    message='Номер телефону може складатися лише з цифр!.')], verbose_name='Телефонний номер менеджера:',
                                    help_text='Формат для телефонного номера: 0XXXXXXXXX (напр.: 0982548248)')
    user_manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Користувач (User) якому належить телефонний',
                                                                  help_text='Може бути не вказаний!')

    def __str__(self):
        return self.phone_manager

    class Meta:
        verbose_name = "Телефонний номер менеджера"
        verbose_name_plural = "Телефонні номера менеджерів"




class Emailwebservice(models.Model):
    true_false_char = ((True, 'True'), (False, 'False'))
    email_use_tls = models.BooleanField(null=False, blank=False, max_length=5, choices=true_false_char, default=True, verbose_name='EMAIL_USE_TLS')
    email_host = models.CharField(null=False, blank=False, max_length=64, verbose_name='EMAIL_HOST')
    email_port = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='EMAIL_PORT')
    email_host_user = models.CharField(null=False, blank=False, max_length=64, verbose_name='EMAIL_HOST_USER')
    email_host_password = models.CharField(null=False, blank=False, max_length=64, verbose_name='EMAIL_HOST_PASSWORD')
    default_from_email = models.CharField(null=True, blank=True, max_length=64, verbose_name='DEFAULT_FROM_EMAIL')
    default_to_email = models.CharField(null=True, blank=True, max_length=64, verbose_name='DEFAULT_TO_EMAIL')


    def __str__(self):
        return self.email_host_user

    class Meta:
        verbose_name = "Параметри поштового клієнта"
        verbose_name_plural = "Параметри поштових клієнтів"


class Systemoptions(models.Model):
    email_send = models.BooleanField(null=True, blank=True, default=True, verbose_name="Розсилати email'и при отриманні заказу?",
                                     help_text="Якщо відміченно, то на всі Email адреси, що виділенні нижче будуть вілісланні електронні листи з інформацією про заказ",)
    emails_pool = models.ManyToManyField(Emailstaff, db_index=True, blank=True, verbose_name="Перелік електронних адресів (Emails)")
    phone_send = models.BooleanField(null=True, blank=True, default=True, verbose_name="Розсилати СМС при отриманні заказу?",
                                     help_text="Якщо відміченно, то на всі телефонні номери, що виділенні нижче будуть вілісланні СМС про новий заказ"
                                               "УВАГА! Послуга платна! По СМС неможливо відправити повну інформацію про заказ: тому рекомендується використовувавти в парі з Email інформуванням",)
    phones_pool = models.ManyToManyField(Phonestaff, db_index=True, blank=True, verbose_name="Перелік телефонних номерів")
    email_from = models.ForeignKey(Emailwebservice, db_index=True, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Email з якого надходитимуть електронні листи інформування")


    class Meta:
        verbose_name = "Службові опції"
        verbose_name_plural = "Службові опції"

    def get_email_pool(self):
        return ",\n".join([str(e) for e in self.emails_pool.all()])

    get_email_pool.short_description = "Список Email'ів"

    def get_phone_pool(self):
        return ",\n".join([str(p) for p in self.phones_pool.all()])

    get_phone_pool.short_description = "Список номерів"





