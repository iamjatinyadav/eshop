from django import template

register = template.Library()

@register.simple_tag
def my_tag(data):
    val1=data[0]
    val2 = data[-1]
    return {'first': val1, 'second': val2}
            

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price