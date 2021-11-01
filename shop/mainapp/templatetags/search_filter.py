from collections import defaultdict

from django import template
from django.utils.safestring import mark_safe

from specifications.models import ProductCharacteristics

register = template.Library()


@register.filter
def product_spec(category):
    product_characteristics = ProductCharacteristics.objects.filter(product__category=category)
    characteristic_and_values = defaultdict(list)
    for product_characteristic in product_characteristics:
        if product_characteristic.value not in characteristic_and_values[(product_characteristic.characteristic.characteristic_name, product_characteristic.characteristic.characteristic_filter_name)]:
            characteristic_and_values[
                (product_characteristic.characteristic.characteristic_name, product_characteristic.characteristic.characteristic_filter_name)
            ].append(product_characteristic.value)
    print(characteristic_and_values)
    search_filter_body = """<div class="col-md-12">{}</div>"""
    mid_res = ""
    for (characteristic_name, characteristic_filter_name), characteristic_values in characteristic_and_values.items():
        characteristic_name_html = f"""<p>{characteristic_name}</p>"""
        characteristic_values_res = ""
        for f_v in characteristic_values:
            mid_characteristic_values_res = \
                "<input type='checkbox' name='{f_f_name}' value='{characteristic_name}'> {characteristic_name}</br>".format(
                    characteristic_name=f_v, f_f_name=characteristic_filter_name
                )
            characteristic_values_res += mid_characteristic_values_res
        characteristic_name_html += characteristic_values_res
        mid_res += characteristic_name_html + '<hr>'
    res = search_filter_body.format(mid_res)
    return mark_safe(res)
