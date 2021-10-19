from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class FishRodAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">Загружайте изображение с минимальным разрешением {}X{}</span> '.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МБ!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image


class FishRodAdmin(admin.ModelAdmin):

    form = FishRodAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='FishRods'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FishLineAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='FishLines'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(FishRod, FishRodAdmin)
admin.site.register(FishLine, FishLineAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)