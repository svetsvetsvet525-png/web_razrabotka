from django.db import models
from django.urls import reverse


class Employees(models.Model):
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=100, null=False)
    patronymic = models.DateField(null=True)
    age = models.IntegerField()
    date_of_bird = models.DateField(null=False)
    salary = models.FloatField(null=False)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('keyboard', 'Клавиатуры'),
        ('mouse', 'Мыши'),
        ('headset', 'Наушники'),
        ('monitor', 'Мониторы'),
    ]

    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='keyboard')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True, allow_unicode=True, blank=True)
    brand = models.CharField('Бренд', max_length=100, default='—')
    price = models.PositiveIntegerField('Цена, ₽')
    old_price = models.PositiveIntegerField('Старая цена, ₽', null=True, blank=True)
    sku = models.CharField('Артикул', max_length=50, blank=True)
    stock = models.PositiveIntegerField('Остаток, шт', default=1)
    image = models.CharField('Путь к изображению', max_length=300, blank=True,
                             help_text='Например: /static/img/k55-main.webp')
    short_description = models.CharField('Краткое описание', max_length=300, blank=True)
    description = models.TextField('Описание', blank=True)
    specs = models.TextField('Характеристики', blank=True,
                             help_text='Каждая строка в формате: Поле: значение')
    rating = models.FloatField('Рейтинг', default=0)
    review_count = models.PositiveIntegerField('Отзывов', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def specs_list(self):
        rows = []
        for line in self.specs.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                rows.append((key.strip(), value.strip()))
        return rows

    @property
    def discount(self):
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return 0
