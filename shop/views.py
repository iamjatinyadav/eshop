
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Max
from django.urls import reverse_lazy

from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from shop.forms import *
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

class HandleRegister(FormView):
    template_name = 'multishop/register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        print("hey")
        form = self.get_form()
        if form.is_valid():
            print("hi")
            is_active = True
            form.save()
            print("hello")
            return render(request, 'multishop/login.html')
        else:
            print("inh")
            context={'val':self.form_invalid(form)}
            return render(request, 'multishop/register.html', context)



class HandleLogin(LoginView):
    template_name = "multishop/login.html"



class Handlelogout(LogoutView):
    template_name = "multishop/index.html"
    

class AddToCart(CreateView):
    success_url = "multishop/detail.html"

    def get(self, request, *args, **kwargs):
        
        if str(request.user) != "AnonymousUser":
            print(kwargs.get('id'))
            print(kwargs.get('arg'))
            product =[ i.product.id for i in Cart.objects.get(user__email = request.user).carts_items.all()]
            if  int(kwargs.get('id')) in product:
                p = Cart.objects.get(user__email = request.user).carts_items.filter(product_id = int(kwargs.get('id')))
                for z in p:
                    z.count += int(kwargs.get('arg'))
                    z.save()
                return redirect('cart')

            else:
                user = Cart.objects.get(user__email = request.user)
                p=Product.objects.get(id = int(kwargs.get('id')))
                
                cartitems = CartItems(cart = user, product= p, count= int(kwargs.get('arg')))
                cartitems.save()
                return redirect('cart')

                

class ShowCartItems(ListView):
    template_name = "multishop/cart.html"

    def get(self, request):

        if str(request.user) != "AnonymousUser":
            cart_owner = Cart.objects.get(user__email =request.user)
            cart_item = CartItems.objects.filter(cart= cart_owner)
            total = Cart.total_value(self, request, cart_owner)
            context = {'query': cart_item, 'total':total['total_price__sum']}
            return render(request, "multishop/cart.html" ,context)
        
        else:
            return render(request,"multishop/cart.html")
            
        
        
def delete_cart_value(request, pk):
    if str(request.user) != "AnonymousUser":
        # user = request.user
        get_val = CartItems.objects.get(id=pk)
        get_val.delete()
        return redirect("cart")



def update_cart_value(request, pk, val):
    if str(request.user) != "AnonymousUser":
        get_val = CartItems.objects.get(id=pk)
        if val == 'plus':
            get_val.count += 1
            get_val.save()
        else:
            if get_val.count == 1:
                get_val.delete()
            else:
                get_val.count -= 1
                get_val.save()

        return redirect("cart")
                        

    
        




    

