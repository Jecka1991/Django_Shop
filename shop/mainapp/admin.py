from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from .models import *

from PIL import Image


class FishRodAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображение с минимальным разрешением {}X{}'.format(
            *self.MIN_RESOLUTION
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min.width, min.height = self.MIN_RESOLUTION
        if img.height < min.height or img.width < min.width:
            raise ValidationError('Разрешение изображения меньше минимального!')
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