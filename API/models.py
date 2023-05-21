from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms


class TimeMixin(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        abstract = True


class Products(TimeMixin):
    spu_id = models.CharField(verbose_name='SPU', max_length=512, unique=True)
    override_title = models.CharField(verbose_name='Название', max_length=255, null=True, blank=True)
    override_brand = models.CharField(verbose_name='Бренд', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '#' + self.spu_id
