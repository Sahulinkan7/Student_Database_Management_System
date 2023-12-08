from django.shortcuts import render 
from .forms import AttendanceCheckForm,FeedbackForm,LeaveForm
from .models import Courses,Subjects,Students,Attendance,AttendanceReport,FeedbackStudent,LeaveReportStudent
from django.contrib import messages
from .decorators import checklogindecorator2
from django.contrib.auth.decorators import login_required
from django import forms 

def subjectchoicelist(course):
    subjects=Subjects.objects.filter(course=course)
    choice_list=[]
    for i in subjects:
        choice_list.append((i.id,i.subject_name))
    return choice_list


@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['3'])
def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    total_attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    total_attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=student_obj.course
    subjects_data=Subjects.objects.filter(course=course)
    subjects_count=subjects_data.count()
    attendance_present=[]
    attendance_absent=[]
    for subject in subjects_data:
        attendance=Attendance.objects.filter(subject_id=subject)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj).count()
        attendance_present.append(attendance_present_count)
        attendance_absent.append(attendance_absent_count)
        
    context={"total_attendance":attendance_total,"total_present":total_attendance_present,
             "total_absent":total_attendance_absent,"subjects_count":subjects_count,"subjects":subjects_data,
             "attendance_present_count":attendance_present,"attendance_absent_count":attendance_absent}
    return render(request,"student/student_home.html",context)

@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['3'])
def show_my_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course
    choice_list=subjectchoicelist(course)
    attendance_reports=None
    if request.method=='POST':
        fm=AttendanceCheckForm(request.POST)
        fm.fields['subject'].choices=choice_list
        if fm.is_valid():
            start_date=fm.cleaned_data['start_date']
            end_date=fm.cleaned_data['end_date']
            subject=fm.cleaned_data['subject']
            print(start_date,end_date,subject)
            subject_obj=Subjects.objects.get(id=subject)
            student_obj=Students.objects.get(admin=request.user.id)
            attendance_obj=Attendance.objects.filter(attendance_date__range=(start_date,end_date),subject_id=subject_obj)
            attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance_obj,student_id=student_obj)
            # messages.success(request,"data fetched")
    else:
        fm=AttendanceCheckForm()
    fm.fields['subject'].choices=choice_list
    return render(request,"student/my_attendance.html",{'form':fm,'attendance_reports':attendance_reports})

@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['3'])
def student_feedback(request):
    student_obj=Students.objects.get(admin=request.user.id)
    feedback_data=FeedbackStudent.objects.filter(student_id=student_obj)
    if request.method=='POST':
        fm=FeedbackForm(request.POST)
        if fm.is_valid():
            feedback_msg=fm.cleaned_data['feedback_message']
            student_obj=Students.objects.get(admin=request.user.id)
            
            try:
                feedback_obj=FeedbackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
                feedback_obj.save()
                fm=FeedbackForm()
                messages.success(request,"Feedback saved successfully !")
            except:
                messages.error(request,"Error occured : feedback not saved")
    else:
        fm=FeedbackForm()
    return render(request,"student/student_feedback.html",{'form':fm,'feedback_data':feedback_data})


@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['3'])
def student_leave(request):
    student_obj=Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=student_obj)
    if request.method=='POST':
        fm=LeaveForm(request.POST)
        if fm.is_valid():
            leave_date=fm.cleaned_data['date']
            reason=fm.cleaned_data['reason']
            student_obj=Students.objects.get(admin=request.user.id)
            try:
                try:
                    applied_dates=LeaveReportStudent.objects.filter(student_id=student_obj,leave_date=leave_date)
                    if applied_dates:
                        raise forms.ValidationError("You have already applied leave on this date")
                    leave_obj=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=reason,leave_status=0)
                    leave_obj.save()
                    fm=LeaveForm()
                    messages.success(request,f"you applied for leave on {leave_date} for reason {reason}")
                except:
                    messages.error(request,"you have already applied on this date")
            except:
                messages.error(request,"some error occurred !")
    else:
        fm=LeaveForm()
    return render(request,"student/student_leave.html",{'form':fm,'leave_data':leave_data})