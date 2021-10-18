from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *


class FishRodAdmin(admin.ModelAdmin):

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