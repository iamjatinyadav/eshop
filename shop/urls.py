from django.urls import path, include
from shop.views import *


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('Products', CategoryView.as_view(), name="products"),
    path('<slug:slug>/Products', CategoryProductView.as_view(), name="category-products"),
    path('products/<str:category>/<int:Min>-<str:Max>', FilterPriceView.as_view(), name="price-product"),
    path('product/<slug:slug>', ProductView.as_view(), name="product-detail"),
    path('contact', ContactView.as_view(), name="contact"),
    path('Login', HandleLogin.as_view(), name="login"),
    path('Logout', Handlelogout.as_view(), name="logout"),
    path('addtocart/<slug:id>/<int:arg>', AddToCart.as_view(), name = "addtocart"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('cart', ShowCartItems.as_view(), name = "cart"),
    path('delete_value/<int:pk>', delete_cart_value, name = "deletecart"),
    path('update_value/<int:pk>/<str:val>', update_cart_value , name = "updatecart"),

]
