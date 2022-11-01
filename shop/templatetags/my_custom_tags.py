from django import template

register = template.Library()

@register.simple_tag
# lst2=[[0, 200], [200, 400], [400, 600], [600, 800], [800]]
def my_tag(data):
    # print(args)
    # for lst1 in lst2:
        # for lst in lst1:
    val1=data[0]
    val2 = data[-1]
    return {'first': val1, 'second': val2}
            # print(lst)
# print(my_tag(lst2))