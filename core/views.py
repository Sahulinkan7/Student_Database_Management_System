from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def changepassword(request):
    if request.method=='POST':
        fm=PasswordChangeForm(data=request.POST,user=request.user)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,request.user)
            messages.success(request,"your password has been changed.")
            return HttpResponseRedirect(reverse("dashboard_view"))
    else:
        fm=PasswordChangeForm(user=request.user)
    return render(request,"core/change_password.html",{'form':fm})