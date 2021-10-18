from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(FishRod)
admin.site.register(FishLine)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)