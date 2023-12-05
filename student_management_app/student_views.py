from django.shortcuts import render 

def student_home(request):
    print("hello am deepak in student home")
    return render(request,"student/student_home.html")