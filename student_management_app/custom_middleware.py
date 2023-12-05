from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type=='1':
                if modulename=="student_management_app.adminviews":
                    print(modulename)
                if modulename=="student_management_app.views":
                    pass
                else:
                    print(request.path)
                    messages.error(request,"Permission denied : You can only access admin pages")
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type=='2':
                if modulename=="student_management_app.staff_views":
                    print(modulename)
                if modulename=="student_management_app.views":
                    pass
                else:
                    print(request.path)
                    messages.error(request,"Permission denied : You can only access staff pages")
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type=='3':
                if modulename=="student_management_app.student_views":
                    print(modulename)
                if modulename=="student_management_app.views":
                    pass
                else:
                    messages.error(request,"Permission denied : You can only access student pages")
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("login_view"))
        else:
            if request.path == reverse("login_view") or request.path==reverse("admin_home"):
                pass
            else:
                return HttpResponseRedirect(reverse("login_view"))