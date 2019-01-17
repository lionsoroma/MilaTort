from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum


class Comment(models.Model):
    r_commit = models.TextField(max_length=1024, db_index=True, null=True, blank=True, verbose_name='Відгук / коментар', help_text="Ваш коментар")
    client_commit = models.ForeignKey("main.Client", null=True, db_index=True, blank=False, on_delete=models.SET_NULL,
                                      verbose_name='Хто залишив відгук')
    product_commit = models.ForeignKey("products.Product", null=True, db_index=True, blank=False, on_delete=models.SET_NULL, verbose_name='Відгук до продукту / події')
    dates_commit = models.DateTimeField(null=True, blank=True, db_index=True, auto_now_add=True, auto_now=False,
                                        verbose_name='Дата')
    dates_edit = models.DateTimeField(null=True, blank=True, auto_now_add=False, auto_now=True,
                                         verbose_name='Дата останьої редакції')
    rating = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10), MinValueValidator(0)],
                                           help_text='Оцінка продукту: залишає клієнт, макс. значення - 10 од.',
                                           verbose_name='Оцінка продукту')

    def __str__(self):
        return self.r_commit

    def save(self, *args, **kwargs):
        if not self.id:
            if self.product_commit.average_rating:
                count_of_rating = Comment.objects.filter(product_commit=self.product_commit, rating__gte=0).count()
                if count_of_rating:
                    sum_rating = Comment.objects.filter(product_commit=self.product_commit, rating__gte=0).aggregate(Sum('rating'))
                    average_rating = round(sum_rating['rating__sum'] / count_of_rating)
                    self.product_commit.average_rating = average_rating
                    self.product_commit.save()
            else:
                self.product_commit.average_rating = self.rating
                self.product_commit.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Відгук / коментар"
        verbose_name_plural = "Відгуки / коментарі"



