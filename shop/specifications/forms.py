from django import forms

from mainapp.models import Category
from .models import CharacteristicValidator, CategoryCharacteristic


class NewCategoryCharacteristicKeyForm(forms.ModelForm):

    class Meta:
        model = CategoryCharacteristic
        fields = '__all__'


class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class CharacteristicValidatorForm(forms.ModelForm):

    class Meta:
        model = CharacteristicValidator
        fields = ['category']
