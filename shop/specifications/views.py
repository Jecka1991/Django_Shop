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
        return render(request, 'product_characteristic.html', {})


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

