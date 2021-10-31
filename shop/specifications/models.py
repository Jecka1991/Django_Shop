from django.db import models


class CategoryCharacteristic(models.Model):

    category = models.ForeignKey("mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE)
    characteristic_name = models.CharField(verbose_name='Название ключа для категории', max_length=50)
    characteristic_filter_name = models.CharField(verbose_name='Название для фильтра', max_length=50)
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'characteristic_name', 'characteristic_filter_name')

    def __str__(self):
        return f"{self.category.name} | {self.characteristic_name}"


class CharacteristicValidator(models.Model):

    category = models.ForeignKey("mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE)
    characteristic_key = models.ForeignKey(CategoryCharacteristic, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    valid_characteristic_value = models.CharField(max_length=100, verbose_name='Значение характеристики')

    def __str__(self):
        return f"Категория {self.category.name} | " \
               f"Характристика {self.characteristic_key.characteristic_name} | " \
               f"Значение характеристики {self.valid_characteristic_value}"


class ProductCharacteristics(models.Model):

    product = models.ForeignKey("mainapp.Product", verbose_name='Товар', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(CategoryCharacteristic, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f"Товар - {self.product.title} | " \
               f"Характеристика - {self.characteristic.characteristic_name} | " \
               f"Значение - {self.value}"

