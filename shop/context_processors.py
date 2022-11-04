from shop.models import Cart

def cartvalue(request):
    if str(request.user) != "AnonymousUser":
        value= Cart.objects.get(user__email= request.user)
        print(value.cart_items_count)
        return {'total_count': value.cart_items_count}
    else:
        return {'total_count' :0}