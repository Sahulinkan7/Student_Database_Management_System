from django.shortcuts import render ,HttpResponse
from django.http import JsonResponse
from .models import Subjects,Staffs,Sessionyearmodel,Students,Attendance,AttendanceReport,LeaveReportStaff,FeedbackStaffs
from .decorators import checklogindecorator2
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib import messages
from .forms import LeaveForm,FeedbackForm

def staff_home(request):
    return render(request,"staff/staff_home.html")


@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def take_attendance(request):
    sessions=Sessionyearmodel.objects.all()
    subjects=Subjects.objects.filter(staff=request.user.id)
    return render(request,"staff/take_student_attendance.html",{'sessions':sessions,'subjects':subjects})

@csrf_exempt
@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def get_students(request):
    data=json.loads(request.body)
    subject_id=data['subject']
    session_year=data['session_year']
    # subject_id=request.POST.get("subject")
    # session_year=request.POST.get("session")
    print(subject_id,session_year)
    subject=Subjects.objects.get(id=subject_id)
    session_year=Sessionyearmodel.objects.get(id=session_year)
    students=Students.objects.filter(course=subject.course,session_year=session_year)
    students_data=serializers.serialize("python",students)
    student_list=[]
    for student in students:
        data={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        student_list.append(data)
    return JsonResponse(json.dumps(student_list),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    data2=json.loads(request.body)
    subject_id=data2['subject_id']
    attendance_date=data2['attendance_date']
    students_ids=data2['students_ids']
    session_year_id=data2['session_year_id']
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=Sessionyearmodel.objects.get(id=session_year_id)
    attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year=session_model)
    attendance.save()
    for student in students_ids:
        stu = Students.objects.get(admin=student['id'])
        attendance_report=AttendanceReport(student_id=stu,attendance_id=attendance,status=student['status'])
        attendance_report.save()
    messages.success(request,"attendance saved for this subject !")
    return HttpResponse("ok")


def staff_leave(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    if request.method=='POST':
        fm=LeaveForm(request.POST)
        if fm.is_valid():
            leave_date=fm.cleaned_data['date']
            reason=fm.cleaned_data['reason']
            staff_obj=Staffs.objects.get(admin=request.user.id)
            try:
                leave_obj=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=reason,leave_status=0)
                leave_obj.save()
                messages.success(request,f"you applied for leave on {leave_date} for reason {reason}")
            except:
                messages.error(request,"some error occurred !")
    else:
        fm=LeaveForm()
    return render(request,"staff/staff_leave.html",{'form':fm,'leave_data':leave_data})


def staff_feedback(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedbackStaffs.objects.filter(staff_id=staff_obj)
    if request.method=='POST':
        fm=FeedbackForm(request.POST)
        if fm.is_valid():
            feedback_msg=fm.cleaned_data['feedback_message']
            staff_obj=Staffs.objects.get(admin=request.user.id)
            
            try:
                feedback_obj=FeedbackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
                feedback_obj.save()
                fm=FeedbackForm()
                messages.success(request,"Feedback saved successfully !")
            except:
                messages.error(request,"Error occured : feedback not saved")
    else:
        fm=FeedbackForm()
    return render(request,"staff/staff_feedback.html",{'form':fm,'feedback_data':feedback_data})