from dataclasses import fields
from django.forms import ModelForm
from shop.models import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__" 