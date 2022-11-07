from enum import auto
import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel, AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
# Create your models here.

class Contact(TimeStampedModel):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    name = models.CharField(max_length = 255, null=True, blank = True)
    email = models.EmailField(max_length = 254, null = True, blank = True)
    subject = models.CharField(max_length = 255, null=True, blank = True)
    message = models.TextField(max_length =2000, null= True, blank = True)

    class Meta:
        verbose_name = "Contacts"
        verbose_name_plural = "Contacts"
        db_table = "Contacts_table"

    def __str__(self) :
        return "message by "+ self.name



class Category(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    image = models.FileField(upload_to='category_image/',max_length=200, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    parent = TreeForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name='categorys')


    class MPTTMeta:
        order_insertion_by= ['name']

    class Meta:
        verbose_name = 'Categorys'
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.name


    @property
    def total_products_count(self):
        total_product = self.products.all().count()
        return total_product


class Product(TimeStampedModel):
    name = models.CharField(max_length = 255, null=True, blank= True)
    original_price = models.FloatField(max_length = 255, null=True, blank=True)
    discount_persent = models.IntegerField( null=True, blank=True, help_text="Please put any value between 1 to 100")
    discount_price = models.FloatField(max_length = 255, null = True, blank = True, editable=False)
    image = models.FileField(upload_to="products_image/", max_length = 200, null=True, blank=True)
    slug = AutoSlugField(populate_from = 'name',null = True, blank  = True, editable=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank = True, related_name='products')

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = "Products" 
        ordering = ["id"]

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        
        self.discount_price = self.original_price-(self.original_price*self.discount_persent/100)
        super(Product, self).save(*args, **kwargs)




class Cart(TimeStampedModel):
    user = models.ForeignKey(User , on_delete= models.CASCADE, related_name = 'carts')
    is_paid = models.BooleanField(default = False)


    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = "Cart"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.user.email


    @property
    def cart_items_count(self):
        total = 0
        # total_count = self.carts_items.all().count()
        for counts in self.carts_items.all():
            total += counts.count
        return total


    
    @staticmethod
    def total_value(self, request, obj):
        print(request.user)
        total = obj.carts_items.all().aggregate(Sum('total_price'))
        return total
        
# def create_cart(sender, instance, created, **kwargs):
#     if created:
#         Cart.objects.create(user = instance)
#         print("cart created")

# post_save.connect(create_cart, sender=User)


    

class CartItems(TimeStampedModel):
    cart = models.ForeignKey('Cart', on_delete= models.CASCADE, related_name = 'carts_items')
    product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, blank = True , related_name = 'products')
    count = models.IntegerField(null=True, blank = True)
    total_price = models.FloatField(max_length = 255, null=True, blank=True)


    class Meta:
        verbose_name = 'Cart_Values'
        verbose_name_plural = 'Cart_Values'
        ordering = ["id"]

    def __str__(self) -> str:
        return self.cart.user.email + " buy " + self.product.name
    
    

    def save(self, *args, **kwargs):

        self.total_price = self.count * self.product.discount_price
        super(CartItems, self).save(*args, **kwargs)



    

    

    
# class Product_Review(TimeStampedModel):
#     product = models.ForeignKey('Product', on_delete= models.CASCADE, null=True, blank= True, related_name='prodect_review')
    

    


    






