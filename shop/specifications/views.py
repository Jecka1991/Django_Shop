from collections import defaultdict

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse

from .models import CategoryCharacteristic, CharacteristicValidator, ProductCharacteristics
from .forms import NewCategoryCharacteristicKeyForm, NewCategoryForm
from mainapp.models import Category, Product


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_characteristics.html', {})


class CreateNewCharacteristic(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryCharacteristicKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_characteristic.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryCharacteristicKeyForm(request.POST or None)
        if form.is_valid():
            new_category_characteristic_key = form.save(commit=False)
            new_category_characteristic_key.category = form.cleaned_data['category']
            new_category_characteristic_key.characteristic_name = form.cleaned_data['characteristic_name']
            new_category_characteristic_key.save()
        return HttpResponseRedirect('/product-specifications/')


class CreateNewCategory(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.name = form.cleaned_data['name']
            new_category.save()
        return HttpResponseRedirect('/product-specifications/')


class CreateNewCharacteristicValidator(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_validator.html', context)


class CharacteristicChoiceView(View):

    def get(self, request, *args, **kwargs):
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="characteristic-validators" id="characteristic-validators-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        characteristic_key_qs = CategoryCharacteristic.objects.filter(
            category_id=int(request.GET.get('category_id'))
        )
        res_string = ""
        for item in characteristic_key_qs:
            res_string += option.format(value=item.characteristic_name, option_name=item.characteristic_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"result": html_select, "value": int(request.GET.get('category_id'))})


class CreateCharacteristicView(View):

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        characteristic_name = request.GET.get('characteristic_name')
        value = request.GET.get('characteristic_value').strip(" ")
        print(value)
        category = Category.objects.get(id=int(category_id))
        characteristic = CategoryCharacteristic.objects.get(category=category, characteristic_name=characteristic_name)
        existed_object, created = CharacteristicValidator.objects.get_or_create(
            category=category,
            characteristic_key=characteristic,
            valid_characteristic_value=value
        )
        if not created:
            return JsonResponse({
                "error": f"Значение '{value}' уже существует."
            })
        messages.add_message(
            request, messages.SUCCESS,
            f'Значение "{value}" для характеристики '
            f'"{characteristic.characteristic_name}" в категории {category.name} успешно создано'
        )
        return JsonResponse({'result': 'ok'})


class NewProductCharacteristicView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_product_characteristic.html', context)


class SearchProductAjaxView(View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=int(category_id))
        products = list(Product.objects.filter(
            category=category,
            title__icontains=query
        ).values())
        return JsonResponse({"result": products})


class AttachNewCharacteristicToProduct(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        product = Product.objects.get(id=int(request.GET.get('product_id')))
        existing_characteristics = list(set([item.characteristic.characteristic_name for item in product.characteristics.all()]))
        print(existing_characteristics)
        category_characteristics = CategoryCharacteristic.objects.filter(
            category=product.category
        ).exclude(characteristic_name__in=existing_characteristics)
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="product-category-characteristics" id="product-category-characteristics-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        for item in category_characteristics:
            res_string += option.format(value=item.category.id, option_name=item.characteristic_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"characteristics": html_select})


class ProductCharacteristicChoicesAjaxView(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        category = Category.objects.get(id=int(request.GET.get('category_id')))
        characteristic_key = CategoryCharacteristic.objects.get(
            category=category,
            characteristic_name=request.GET.get('product_characteristic_name')
        )
        validators_qs = CharacteristicValidator.objects.filter(
            category=category,
            characteristic_key=characteristic_key
        )
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="product-category-characteristics-choices" id="product-category-characteristics-choices-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        for item in validators_qs:
            res_string += option.format(value=item.id, option_name=item.valid_characteristic_value)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"characteristics": html_select})


class CreateNewProductCharacteristicAjaxView(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(title=request.GET.get('product'))
        category_characteristic = CategoryCharacteristic.objects.get(
            category=product.category,
            characteristic_name=request.GET.get('category_characteristic')
        )
        value = request.GET.get('value')
        characteristic = ProductCharacteristics.objects.create(
            characteristic=category_characteristic,
            product=product,
            value=value
        )
        product.characteristics.add(characteristic)
        return JsonResponse({"OK": "OK"})


class UpdateProductCharacteristicsView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'update_product_characteristics.html', context)


class ShowProductCharacteristicsForUpdate(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=int(request.GET.get('product_id')))
        characteristics_values_qs = product.characteristics.all()
        head = """
        <hr>
            <div class="row">
                <div class="col-md-4">
                    <h4 class="text-center">Характеристика</h4>
                </div>
                <div class="col-md-4">
                    <h4 class="text-center">Текущее значение</h4>
                </div>
                <div class="col-md-4">
                    <h4 class="text-center">Новое значение</h4>
                </div>
            </div>
        <div class='row'>{}</div>
        <div class="row">
        <hr>
        <div class="col-md-4">
        </div>
        <div class="col-md-4">
            <p class='text-center'><button class="btn btn-success" id="save-updated-characteristics">Сохранить</button></p> 
        </div>
        <div class="col-md-4">
        </div>
        </div>
        """
        option = '<option value="{value}">{option_name}</option>'
        select_values = """
            <select class="form-select" name="characteristic-value" id="characteristic-value" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        mid_res = ""
        select_different_values_dict = defaultdict(list)
        for item in characteristics_values_qs:
            fv_qs = CharacteristicValidator.objects.filter(
                category=item.product.category,
                characteristic_key=item.characteristic
            ).values()
            for fv in fv_qs:
                if fv['valid_characteristic_value'] == item.value:
                    pass
                else:
                    select_different_values_dict[fv['characteristic_key_id']].append(fv['valid_characteristic_value'])
            characteristic_field = '<input type="text" class="form-control" id="{id}" value="{value}" disabled/>'
            current_characteristic_value = """
            <div class='col-md-4 characteristic-current-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
                                    """
            body_characteristic_field = """
            <div class='col-md-4 characteristic-name' style='margin-top:10px; margin-bottom:10px;'>{}</div>
                                """
            body_characteristic_field_value = """
            <div class='col-md-4 characteristic-new-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
            """
            body_characteristic_field = body_characteristic_field.format(characteristic_field.format(id=item.characteristic.id, value=item.characteristic.characteristic_name))
            current_characteristic_value_mid_res = ""
            for item_ in select_different_values_dict[item.characteristic.id]:
                current_characteristic_value_mid_res += option.format(value=item.characteristic.id, option_name=item_)
            body_characteristic_field_value = body_characteristic_field_value.format(
                select_values.format(item.characteristic.id, result=current_characteristic_value_mid_res)
            )
            current_characteristic_value = current_characteristic_value.format(characteristic_field.format(id=item.characteristic.id, value=item.value))
            m = body_characteristic_field + current_characteristic_value + body_characteristic_field_value
            mid_res += m
        result = head.format(mid_res)
        return JsonResponse({"result": result})


class UpdateProductCharacteristicsAjaxView(View):

    def post(self, request, *args, **kwargs):
        characteristics_names = request.POST.getlist('characteristics_names')
        characteristics_current_values = request.POST.getlist('characteristics_current_values')
        new_characteristic_values = request.POST.getlist('new_characteristic_values')
        data_for_update = [{'characteristic_name': name, 'current_value': curr_val, 'new_value': new_val} for name, curr_val, new_val
                           in zip(characteristics_names, characteristics_current_values, new_characteristic_values)]
        product = Product.objects.get(title=request.POST.get('product'))
        for item in product.characteristics.all():
            for item_for_update in data_for_update:
                if item.characteristic.characteristic_name == item_for_update['characteristic_name']:
                    if item.value != item_for_update['new_value'] and item_for_update['new_value'] != '---':
                        cf = CategoryCharacteristic.objects.get(
                            category=product.category,
                            characteristic_name=item_for_update['characteristic_name']
                        )
                        item.value = CharacteristicValidator.objects.get(
                            category=product.category,
                            characteristic_key=cf,
                            valid_characteristic_value=item_for_update['new_value']
                        ).valid_characteristic_value
                        item.save()
        messages.add_message(
            request, messages.SUCCESS,
            f'Значения характеристик для товара {product.title} успешно обновлены'
        )
        return JsonResponse({"result": "ok"})


