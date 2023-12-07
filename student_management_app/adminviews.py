from typing import Any
from django.contrib.auth import authenticate,login,logout
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from .forms import ( AddstaffForm,AddCourseForm,AddStudentForm,AddSubjectForm,EditStaffForm,EditStudentForm,
                    EditCourseForm,EditSubjectForm,AddSessionForm)
from .models import CustomUser,Courses,Subjects,Staffs,Students,Sessionyearmodel,FeedbackStudent,FeedbackStaffs
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse
from .decorators import checklogindecorator,checklogindecorator2
from django.utils.decorators import method_decorator
import json


@login_required(login_url="/")
@checklogindecorator
def add_student_view(request):
    if request.method=='POST':
        fm=AddStudentForm(request.POST)
        if fm.is_valid():
            fname=fm.cleaned_data['first_name']
            lname=fm.cleaned_data['last_name']
            email=fm.cleaned_data['email']
            address=fm.cleaned_data['address']
            gender=fm.cleaned_data['gender']
            course=fm.cleaned_data['course']
            session_year_id=fm.cleaned_data['session_year']
            password=email+'ssvm'
            username=email
            try:
                user=CustomUser.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course)
                user.students.course=course_obj
                session_modelobj=Sessionyearmodel.objects.get(id=session_year_id)
                user.students.session_year=session_modelobj
                user.students.gender=gender
                user.students.profile_pic=''
                user.save()
                fm=AddStudentForm()
                messages.success(request,"Student data saved")
            except:
                messages.error(request,"unable to save ! ")
    else:
        fm=AddStudentForm()
    return render(request,"admin/add_student.html",{'form':fm})


@login_required(login_url="/")
@checklogindecorator
def add_staff_view(request):
    if request.method=='POST':
        fm=AddstaffForm(request.POST)
        if fm.is_valid():
            fname=fm.cleaned_data['first_name']
            lname=fm.cleaned_data['last_name']
            email=fm.cleaned_data['email']
            address=fm.cleaned_data['address']
            password=email+"ssvm"
            username=email
            user=CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email,user_type=2)
            user.staffs.address=address
            user.save()
            print("data saved successfully ! ")
            messages.success(request,"Staff saved successfully ! ")
            return HttpResponseRedirect(reverse("manage_staffs"))      
    else:
        fm=AddstaffForm()
    return render(request,"admin/add_staff.html",{'form':fm})

@login_required(login_url="/")
@checklogindecorator
def add_course_view(request):
    if request.method=='POST':
        fm=AddCourseForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Course saved successfully ! ")
            fm=AddCourseForm()
        else:
            messages.error(request,"data not saved. please check")
    else:
        fm=AddCourseForm()
    return render(request,"admin/add_course.html",{'form':fm})


@login_required(login_url="/")
@checklogindecorator
def add_subject_view(request):
    if request.method=='POST':
        fm=AddSubjectForm(request.POST)
        if fm.is_valid():
            subject_name=fm.cleaned_data['subject_name']
            course_id=fm.cleaned_data['course']
            staff_id=fm.cleaned_data['staff']
            try:
                staff_obj=CustomUser.objects.get(id=staff_id)
                course_obj=Courses.objects.get(id=course_id)
                subject=Subjects(subject_name=subject_name,staff=staff_obj,course=course_obj)
                subject.save()
                messages.success(request,"subject added successfully ! ")
            except:
                messages.error(request,"subject not added , please check")                
    else:
        fm=AddSubjectForm()
    return render(request,"admin/add_subject.html",{'form':fm})

@login_required(login_url="/")
@checklogindecorator
def edit_staff_view(request,staff_id):
    usr=CustomUser.objects.get(id=staff_id)
    if request.method=='POST':
        fm=EditStaffForm(data=request.POST,instance=usr)
        if fm.is_valid():
            first_name=fm.cleaned_data['first_name']
            last_name=fm.cleaned_data['last_name']
            email=fm.cleaned_data['email']
            username=fm.cleaned_data['username']
            address=fm.cleaned_data['address']
            
            try:
                staff=CustomUser.objects.get(id=staff_id)
                staff.first_name=first_name
                staff.last_name=last_name
                staff.email=email
                staff.username=username
                staff.save()
                
                staff_model=Staffs.objects.get(admin=staff.staffs.admin)
                staff_model.address=address
                staff_model.save()
                messages.success(request,f"data updated for {staff.first_name} successfully ")
            except:
                messages.error(request,"could not save this data")
    else:
        data={
            'username':usr.username,
            'first_name':usr.first_name,
            'last_name':usr.last_name,
            'email':usr.email,
            'address':usr.staffs.address
        }
        fm=EditStaffForm(data)
    return render(request,"admin/edit_staff.html",{'form':fm,'staff_id':staff_id,'staff':usr})


@login_required(login_url="/")
@checklogindecorator
def edit_student_view(request,pk):
    usr=CustomUser.objects.get(id=pk)
    courses=Courses.objects.all()
    if request.method=='POST':
        fm=EditStudentForm(data=request.POST,instance=usr)
        if fm.is_valid():
            address=fm.cleaned_data['address']
            gender=fm.cleaned_data['gender']
            course=fm.cleaned_data['course']
            session_year=fm.cleaned_data['session_year']
            try:
                course_model=Courses.objects.get(id=course)
                student_object=Students.objects.get(admin=usr.id)
                student_object.address=address
                student_object.gender=gender
                student_object.course=course_model
                session_modelobj=Sessionyearmodel.objects.get(id=session_year)
                student_object.session_year=session_modelobj
                fm.save()
                student_object.save()
                messages.success(request,f"Data updated for {usr.first_name} !")
            except:
                messages.error(request, "data not saved")              
    else:
        fm=EditStudentForm(instance=usr)
        fm.fields['course'].initial=usr.students.course.id
        fm.fields['address'].initial=usr.students.address
        fm.fields['gender'].initial=usr.students.gender
        fm.fields['session_year'].initial=usr.students.session_year.id
    return render(request,"admin/edit_student.html",{'form':fm,'student':usr,'courses':courses})

@login_required(login_url="/")
@checklogindecorator
def edit_course_view(request,course_id):
    course_object=Courses.objects.get(pk=course_id)
    if request.method=='POST':
        fm=EditCourseForm(data=request.POST,instance=course_object)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Course updated successfully .")
        else:
            messages.error(request,"course name updation failed !")
    else:
        fm=EditCourseForm(instance=course_object)
    return render(request,"admin/edit_course.html",{'form':fm})

@login_required(login_url="/")
@checklogindecorator
def edit_subject_view(request,subject_id):
    subject_object=Subjects.objects.get(id=subject_id)
    staffs=Staffs.objects.all()
    if request.method=='POST':
        fm=EditSubjectForm(data=request.POST,instance=subject_object)
        if fm.is_valid():
            staff_id=request.POST.get('staff')
            staff_obj=CustomUser.objects.get(id=staff_id)
            fm.save()
            subject_object.staff=staff_obj
            subject_object.save()
            messages.success(request,"Subject got updated ! ")
        else:
            messages.error(request,"Subject updation failed ! ")
    else:
        fm=EditSubjectForm(instance=subject_object)
    return render(request,"admin/edit_subject.html",{'form':fm,'staffs':staffs,'subject':subject_object})


@method_decorator(login_required(login_url="/"),name="dispatch")
class manage_session_view(FormView):
    form_class=AddSessionForm
    template_name="admin/manage_sessions.html"
    success_url="/manage_sessions/"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['sessions'] = Sessionyearmodel.objects.all()
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        return super().form_valid(form)

@method_decorator(login_required(login_url="/"),name='dispatch')
@method_decorator(checklogindecorator2(allowed_roles=["2","1"]),name='dispatch')
class manage_courses_view(ListView):
    model=Courses
    template_name='admin/manage_courses.html'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['course_count']=Courses.objects.all().count()
        return context

@method_decorator(login_required(login_url="/"),name='dispatch')
@method_decorator(checklogindecorator2(allowed_roles=["2","1"]),name='dispatch')
class manage_staffs_view(ListView):
    model=CustomUser
    template_name='admin/manage_staffs.html'
    context_object_name='staffs'
    
    def get_queryset(self):
       return CustomUser.objects.filter(user_type=2)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['staffs_count']=Staffs.objects.all().count()
        return context
    
@method_decorator(login_required(login_url="/"),name='dispatch')
@method_decorator(checklogindecorator2(allowed_roles=["2","1"]),name='dispatch')
class manage_students_view(ListView):
    model=CustomUser
    template_name='admin/manage_students.html'
    context_object_name='students'
    
    def get_queryset(self):
       return CustomUser.objects.filter(user_type=3)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['students_count']=Students.objects.all().count()
        return context
    
@method_decorator(login_required(login_url="/"),name='dispatch')
@method_decorator(checklogindecorator2(allowed_roles=["2","1"]),name='dispatch')
class manage_subjects_view(ListView):
    model=Subjects
    template_name='admin/manage_subjects.html'
    
    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context['subject_count']=Subjects.objects.all().count()
        return context
    
login_required(login_url="/")
checklogindecorator2(allowed_roles=["1"])
def student_feedback_reply(request):
    student_feedbacks=FeedbackStudent.objects.all()
    return render(request,"admin/student_feedback_reply.html",{'feedbacks':student_feedbacks})

@csrf_exempt
def save_student_feedback_reply(request):
    data=json.loads(request.body)
    id=data['feedback_id']
    reply_message=data['reply_message']
    student_feedback_obj=FeedbackStudent.objects.get(id=id)
    student_feedback_obj.feedback_reply=reply_message
    student_feedback_obj.save()
    print(student_feedback_obj.feedback,student_feedback_obj.feedback_reply)
    return HttpResponse("OK")

login_required(login_url="/")
checklogindecorator2(allowed_roles=["1"])
def staff_feedback_reply(request):
    staff_feedbacks=FeedbackStaffs.objects.all()
    return render(request,"admin/staff_feedback_reply.html",{'feedbacks':staff_feedbacks})

@csrf_exempt
def save_staff_feedback_reply(request):
    data=json.loads(request.body)
    id=data['feedback_id']
    reply_message=data['reply_message']
    staff_feedback_obj=FeedbackStaffs.objects.get(id=id)
    staff_feedback_obj.feedback_reply=reply_message
    staff_feedback_obj.save()
    print(staff_feedback_obj.feedback,staff_feedback_obj.feedback_reply)
    return HttpResponse("OK")
    