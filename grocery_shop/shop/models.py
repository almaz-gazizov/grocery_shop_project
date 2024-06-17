import os

from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image


User = get_user_model()

MAX_LEN_NAME = 200
MAX_LEN_STR = 30


class CategorySubcategoryModel(models.Model):
    name = models.CharField(
        max_length=MAX_LEN_NAME, verbose_name='Название'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.name[:MAX_LEN_STR]


class Category(CategorySubcategoryModel):
    image = models.ImageField(
        upload_to='category_images/',
        verbose_name='Изображение категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(CategorySubcategoryModel):
    image = models.ImageField(
        upload_to='subcategory_images/',
        verbose_name='Изображение подкатегории'
    )
    category = models.ForeignKey(
        Category, related_name='subcategories',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    name = models.CharField(
        max_length=MAX_LEN_NAME, verbose_name='Название'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        Subcategory, related_name='products',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=7, decimal_places=2
    )
    image = models.ImageField(upload_to='product_images/original/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_thumbnails()

    def create_thumbnails(self):
        if self.image:
            sizes = {
                'large': (800, 800),
                'medium': (300, 300),
                'small': (100, 100),
            }

            for size in sizes:
                self.resize_image(size, sizes[size])

    def resize_image(self, size_name, size):
        image = Image.open(self.image.path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        image_path = os.path.splitext(self.image.path)
        resized_image_path = f"{image_path[0]}_{size_name}{image_path[1]}"
        image.save(resized_image_path)

    @property
    def image_large(self):
        return self._get_image_by_size('large')

    @property
    def image_medium(self):
        return self._get_image_by_size('medium')

    @property
    def image_small(self):
        return self._get_image_by_size('small')

    def _get_image_by_size(self, size_name):
        image_path = os.path.splitext(self.image.url)
        return f"{image_path[0]}_{size_name}{image_path[1]}"

    class Meta:
        ordering = ('id',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return (
            f'{self.name[:MAX_LEN_STR]} {self.slug}'
            f'{self.category}'
            f'{self.subcategory} {self.price}'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        Product,
        verbose_name='Продукты',
        through='ProductInCart'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'

    def __str__(self):
        return f'{self.user}: {self.products}'


class ProductInCart(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='cartproducts'
    )
    products = models.ForeignKey(
        Product,
        verbose_name='Продукты',
        on_delete=models.CASCADE,
        related_name='cartproducts'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1
    )

    @property
    def total_price(self):
        return self.product.price * self.amount

    class Meta:
        ordering = ('id',)
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'

    def __str__(self):
        return f'{self.products}: {self.amount}'
