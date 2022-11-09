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

class RegisterForm(ModelForm):

    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    
    class Meta:
        model  =User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email= email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password is not None and password != confirm_password:
            self.add_error("confirm password", "Your passwords must match")
        return cleaned_data


   
