from django.contrib import admin
from shop.models import *
from mptt.admin import DraggableMPTTAdmin
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'email', 'subject', 'message']


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ['tree_actions', 'indented_title', 'created', 'modified']
    list_display_links = ['indented_title',]

# admin.site.register(Node, CategoryAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'original_price', 'discount_price', 'category', 'slug'] 


