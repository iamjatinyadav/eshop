
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Max

from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views import View

# Create your views here.
class IndexView(ListView):
    template_name = "multishop/index.html"
    model = Product
    

    def get_context_data(self, **kwargs):
        et=super(IndexView, self).get_context_data(**kwargs)
        et['prod'] = Product.objects.all().order_by('-id')[:8]
        et['fproduct'] = Product.objects.all().order_by('-discount_persent')[:8]
        et['cat'] = Category.objects.all()
        return et

    # def get(self,request, *args, **kwargs):
    #         user = request.user
    #         print(user)

class CategoryView(ListView):
    template_name = "multishop/shop.html"
    model = Category

    def get(self, request, *args, **kwargs):
        lst=[]
        lst2=[]
        lst3=[]
        product = Product.objects.all()
        paginator = Paginator(product, 8) 
        h_price = product.aggregate(Max('discount_price'))
        # print(round(int(h_price['discount_price__max']),-2))
        if int(h_price['discount_price__max']) > 500:
            for i in range(0,int(h_price['discount_price__max']), 200):
                lst2.append(i)
        else:
            for i in range(0,int(h_price['discount_price__max']), 100):
                lst2.append(i)
          
        for idx in range(len(lst2)):
            if idx+1 < len(lst2):
                lst3.append({'first':lst2[idx], 'second':lst2[idx+1]})
            else:
                lst3.append({'first':lst2[idx], 'second': 'Max'})

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for i in range(page_obj.paginator.num_pages):
            lst.append(i+1)

        count = product.count()

        context = {'page_obj': page_obj, 'lst':lst, 'count': count, 'one': 'al', 'lst3': lst3}
        return render(request, 'multishop/shop.html', context)


class CategoryProductView(ListView):

    def get(self, request, *args, **kwargs):
        lst2=[]
        lst3=[]
        cproduct = Product.objects.filter(category__slug=self.kwargs.get('slug'))
        count = cproduct.count()
        h_price = cproduct.aggregate(Max('discount_price'))
        # print(round(int(h_price['discount_price__max']),-2))
        if int(h_price['discount_price__max']) > 500:
            for i in range(0,int(h_price['discount_price__max']), 200):
                lst2.append(i)
        else:
            for i in range(0,int(h_price['discount_price__max']), 100):
                lst2.append(i)
          
        for idx in range(len(lst2)):
            if idx+1 < len(lst2):
                lst3.append({'first':lst2[idx], 'second':lst2[idx+1]})
            else:
                lst3.append({'first':lst2[idx], 'second': 'Max'})

        context = {'page_obj': cproduct, 'count':count, 'one':kwargs.get('slug'), 'lst3': lst3}
        return render(request, 'multishop/shop.html', context)

        
class FilterPriceView(ListView):
    
    def get(self,request, *args, **kwargs):
        Min = kwargs.get('Min')
        Max = kwargs.get('Max')
        # print(Min,Max)
        if Max != "Max":
            if kwargs.get('category')=='al':
                page_obj = Product.objects.filter(discount_price__range=[Min, Max])
            else:
                page_obj = Product.objects.filter(category__slug=kwargs.get('category')).filter(discount_price__range=[Min, Max])
        else:
            if kwargs.get('category')=='al':
                page_obj = Product.objects.filter(discount_price__gt=Min)
            else:
                page_obj = Product.objects.filter(category__slug=kwargs.get('category')).filter(discount_price__gt=Min)
                
        context = {'page_obj': page_obj , 'one':kwargs.get('category')}
        return render(request, 'multishop/shop.html', context)

    

    
class ProductView(DetailView):
    # template_name = "multishop/detail.html"

    def get(self, request, *args, **kwargs):
        # print(kwargs.get('slug'))
        slg= kwargs.get('slug')
        prod = Product.objects.get(slug = kwargs.get('slug'))
        category = prod.category
        related_product = Product.objects.filter(category=category).exclude(slug=slg)
        # print(related_product)
        context = {'product': prod, 'related_product':related_product}
        return render(request, 'multishop/detail.html', context)



class ContactView(TemplateView):
    template_name = "multishop/contact.html"


class Handlelogout(LogoutView):
    # print("hello")
    template_name = "multishop/index.html"
    # def get(self, request, *args, **kwargs):
    #     print("h1")
    #     logout(request)
    #     return redirect("index")

# def handlelogout(request):
#     print("hel")
#     logout(request)
#     print("hello")
#     return redirect("index")

class AddCartItems(ListView):
    template_name = "multishop/cart.html"
    
    def get(self,request):
        if request.user:
            query = CartItems.objects.filter(cart__user = request.user)
            # total = query.total_price
            # print(total)
            context = {'query': query}
            return render(request, "multishop/cart.html" ,context)
        

        
        
        




    

