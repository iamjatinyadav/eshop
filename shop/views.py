from itertools import product
from multiprocessing import context
from pydoc import pager
from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DetailView
from django.core.paginator import Paginator

from .models import *
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


class CategoryView(ListView):
    template_name = "multishop/shop.html"
    model = Category

    def get(self, request, *args, **kwargs):
        lst=[]
        product = Product.objects.all()
        paginator = Paginator(product, 8) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for i in range(page_obj.paginator.num_pages):
            lst.append(i+1)

        count = product.count()

        context = {'page_obj': page_obj, 'lst':lst, 'count': count, 'one': 'al'}
        return render(request, 'multishop/shop.html', context)


class CategoryProductView(ListView):

    def get(self, request, *args, **kwargs):
        cproduct = Product.objects.filter(category__slug=self.kwargs.get('slug'))
        count = cproduct.count()
        context = {'page_obj': cproduct, 'count':count, 'one':kwargs.get('slug')}
        return render(request, 'multishop/shop.html', context)

        
class FilterPriceView(ListView):
    
    def get(self,request, *args, **kwargs):
        Min = kwargs.get('Min')
        Max = kwargs.get('Max')
        # print(Min,Max)
        if kwargs.get('category')=='al':
            page_obj = Product.objects.filter(discount_price__range=[Min, Max])
        else:
            page_obj = Product.objects.filter(category__slug=kwargs.get('category')).filter(discount_price__range=[Min, Max])
        context = {'page_obj': page_obj , 'one':kwargs.get('category')}
        return render(request, 'multishop/shop.html', context)

    # def get(self, request, *args, **kwargs):
    #     pass

    
class ProductView(DetailView):
    # template_name = "multishop/detail.html"

    def get(self, request, *args, **kwargs):
        print(kwargs.get('slug'))
        prod = Product.objects.get(slug = kwargs.get('slug'))
        context = {'product': prod}
        return render(request, 'multishop/detail.html', context)


class ContactView(TemplateView):
    template_name = "multishop/contact.html"


# class IndexView(TemplateView):
#     template_name = "multishop/index.html"

    

