from typing import Any
from django.contrib.auth import authenticate,login,logout
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.views.generic import FormView
from .forms import LoginForm,AddstaffForm,AddCourseForm,AddStudentForm,AddSubjectForm,EditStaffForm,EditStudentForm
from .models import CustomUser,Courses,Subjects,Staffs,Students
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse


def login_view(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=LoginForm(request=request,data=request.POST)
            if fm.is_valid():
                usr=fm.cleaned_data['username']
                pswd=fm.cleaned_data['password']
                user=authenticate(username=usr,password=pswd)
                if user is not None:
                    login(request,user=user)
                    messages.success(request,"Logged in Successfully")
                    return HttpResponseRedirect(reverse("dashboard_view"))
            else:
                messages.error(request,"Invalid Credentials")
        else:
            fm=LoginForm()
        return render(request,"core/login.html",{'form':fm})
    else:
        return HttpResponseRedirect(reverse("dashboard_view"))

@login_required(login_url="/")
def dashboard_view(request):
    if request.user.user_type=='1':
        return render(request,"admin/admin_home.html")
    if request.user.user_type=='2':
        return render(request,"staff/staff_home.html")
    if request.user.user_type=='3':
        return render(request,"student/student_home.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_view"))
