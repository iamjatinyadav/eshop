from django.urls import path, include
from shop.views import *


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('Products', CategoryView.as_view(), name="products"),
    path('<slug:slug>/Products', CategoryProductView.as_view(), name="category-products"),
    path('products/<str:category>/<int:Min>-<int:Max>', FilterPriceView.as_view(), name="price-product"),
    path('product/<slug:slug>', ProductView.as_view(), name="product-detail"),
    path('contact', ContactView.as_view(), name="contact"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),

]

#try to do something