from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from shop.models import *




@receiver(post_save, sender= User)
def make_cart(sender, instance, created,  **kwargs):
    if created:
        print("cart creating")
        Cart.objects.create(user= instance)
        print("cart created")


# @receiver(post_save,sender=User)
# def update_user(sender, instance, created, **kwargs):
#     if created == False:
#         instance.save()
#         print("profile updated!!")




# @receiver(post_save, sender=User)
# def save_cart(sender, instance, **kwargs):
#     instance.Cart.save()
