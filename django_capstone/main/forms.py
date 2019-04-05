from django import forms
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser


class RequestForm(forms.Form):
    url = forms.CharField()
    sender = forms.EmailField()


# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = ('username', 'email')


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields
