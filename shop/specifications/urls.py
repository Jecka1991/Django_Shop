from django.urls import path

from .views import (
    BaseSpecView,
    CreateNewCharacteristic,
    CreateNewCategory,
    CreateNewCharacteristicValidator,
    CharacteristicChoiceView,
    CreateCharacteristicView,
    NewProductCharacteristicView,
    SearchProductAjaxView,
    AttachNewCharacteristicToProduct,
    ProductCharacteristicChoicesAjaxView,
    CreateNewProductCharacteristicAjaxView,
    UpdateProductCharacteristicsView,
    ShowProductCharacteristicsForUpdate,
    UpdateProductCharacteristicsAjaxView,

)

urlpatterns = [
    path('', BaseSpecView.as_view(), name='product-list-for-characteristics'),
    path('new-characteristic/', CreateNewCharacteristic.as_view(), name='new-characteristic'),
    path('new-category/', CreateNewCategory.as_view(), name='new-category'),
    path('new-validator/', CreateNewCharacteristicValidator.as_view(), name='new-validator'),
    path('characteristic-choice/', CharacteristicChoiceView.as_view(), name='characteristic-choice-validators'),
    path('characteristic-create/', CreateCharacteristicView.as_view(), name='create-characteristic'),
    path('new-product-characteristic/', NewProductCharacteristicView.as_view(), name='new-product-characteristic'),
    path('search-product/', SearchProductAjaxView.as_view(), name='search-product'),
    path('attach-characteristic/', AttachNewCharacteristicToProduct.as_view(), name='attach-characteristic'),
    path('product-characteristic/', ProductCharacteristicChoicesAjaxView.as_view(), name='product-characteristic'),
    path('attach-new-product-characteristic/', CreateNewProductCharacteristicAjaxView.as_view(), name='attach-new-product-characteristic'),
    path('update-product-characteristics/', UpdateProductCharacteristicsView.as_view(), name='update-product-characteristics'),
    path('show-product-characteristics-for-update/', ShowProductCharacteristicsForUpdate.as_view(), name='show-product-characteristics-for-update'),
    path('update-product-characteristics-ajax/', UpdateProductCharacteristicsAjaxView.as_view(), name='update-product-characteristics-ajax')

]
