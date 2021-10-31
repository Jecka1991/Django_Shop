from django.urls import path

from .views import (
    BaseSpecView,
    CreateNewCharacteristic,
    CreateNewCategory,
    CreateNewCharacteristicValidator,
    CharacteristicChoiceView,
    CreateCharacteristicView,
    NewProductCharacteristicView,
)

urlpatterns = [
    path('', BaseSpecView.as_view(), name='product-list-for-characteristics'),
    path('new-characteristic/', CreateNewCharacteristic.as_view(), name='new-characteristic'),
    path('new-category/', CreateNewCategory.as_view(), name='new-category'),
    path('new-validator/', CreateNewCharacteristicValidator.as_view(), name='new-validator'),
    path('characteristic-choice/', CharacteristicChoiceView.as_view(), name='characteristic-choice-validators'),
    path('characteristic-create/', CreateCharacteristicView.as_view(), name='create-characteristic'),
    path('new-product-characteristic/', NewProductCharacteristicView.as_view(), name='new-product-characteristic'),
]
