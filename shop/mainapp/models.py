from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model.name.startswith(with_respect_to), reverse=True)
        return products


class LatestProducts:

    object = LatestProductManager


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1200, 1200)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категоря', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Разрешение изображения больше максимального!')
        return image


class FishRod(Product):

    type = models.CharField(max_length=255, verbose_name='Тип удилища')
    length = models.CharField(max_length=255, verbose_name='Длина удилища')
    weight = models.CharField(max_length=255, verbose_name='Вес удилища')
    transport_length = models.CharField(max_length=255, verbose_name='Транспортировочная длина')
    number_of_sections = models.CharField(max_length=255, verbose_name='Количество секций')
    maximum_test = models.CharField(max_length=255, verbose_name='Максимальный тест')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class FishLine(Product):
    type = models.CharField(max_length=255, verbose_name='Тип лески')
    diameter = models.CharField(max_length=255, verbose_name='Диаметр лески')
    breaking_load = models.CharField(max_length=255, verbose_name='Разрывная нагрузка')
    length = models.CharField(max_length=255, verbose_name='Длина лески')
    color = models.CharField(max_length=255, verbose_name='Цвет лески')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)
