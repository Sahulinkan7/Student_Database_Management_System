from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def checklogindecorator(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.user_type=='1':
            return view_func(request,*args,**kwargs)
        else:
            messages.error(request,"permission denied: you are not authorized !")
            return HttpResponseRedirect(reverse("dashboard_view"))
    return wrapper


def checklogindecorator2(allowed_roles=['1']):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            if request.user.user_type in allowed_roles:
                print(request.user.user_type,allowed_roles)
                return view_func(request,*args,**kwargs)
            else:
                print(request.user.user_type,allowed_roles)
                messages.error(request,"permission denied: you are not authorized !")
                return HttpResponseRedirect(reverse("dashboard_view"))
        return wrapper
    return decorator