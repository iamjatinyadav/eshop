from shop.models import Cart

def cartvalue(request):
    value= Cart.objects.get(user__email= request.user)
    val = value.cart_items_count
    return {'cart_items_count': val}