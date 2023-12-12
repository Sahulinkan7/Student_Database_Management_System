from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms 

class PasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(label="new password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label="new password confirmation",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields="__all__"