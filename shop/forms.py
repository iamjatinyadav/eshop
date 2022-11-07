from dataclasses import fields
from django.forms import ModelForm
from shop.models import *
from user.models import *
from django import forms
from django.contrib.auth import authenticate, login, get_user_model



class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__" 


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('pass')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("this email does not exist...")
        if not user.check_password(password):
            raise forms.ValidationError("Invalid Password...")
        if not user.is_active:
            raise forms.ValidationError("this user no longer active..")

        return super(LoginForm, self).clean(*args, **kwargs)



   
