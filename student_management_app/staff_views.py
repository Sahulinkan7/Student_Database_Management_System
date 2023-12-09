from django.shortcuts import render ,HttpResponse
from django.http import JsonResponse
from .models import Subjects,Staffs,Sessionyearmodel,Courses,Students,Attendance,AttendanceReport,LeaveReportStaff,FeedbackStaffs
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
@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def save_attendance_data(request):
    data2=json.loads(request.body)
    subject_id=data2['subject_id']
    attendance_date=data2['attendance_date']
    print("attendance_date is ",attendance_date)
    students_ids=data2['students_ids']
    session_year_id=data2['session_year_id']
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=Sessionyearmodel.objects.get(id=session_year_id)
    attendance_obj=Attendance.objects.filter(subject_id=subject_model,attendance_date=attendance_date,session_year=session_model)
    if attendance_obj:
        print("already taken for this ")
        messages.error(request,"Error : Data can not be saved ! Attendance already taken for this subject on this date")
    else:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year=session_model)
        attendance.save()
        for student in students_ids:
            stu = Students.objects.get(admin=student['id'])
            attendance_report=AttendanceReport(student_id=stu,attendance_id=attendance,status=student['status'])
            attendance_report.save()
        messages.success(request,"attendance saved for this subject !")
    return HttpResponse("ok")


@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def view_update_attendance(request):
    subjects=Subjects.objects.filter(staff=request.user.id)
    sessions=Sessionyearmodel.objects.all()
    courses=Courses.objects.all()
    return render(request,"staff/view_update_attendance.html",{"subjects":subjects,"sessions":sessions,"courses":courses})

@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
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
                fm=LeaveForm()
                messages.success(request,f"you applied for leave on {leave_date} for reason {reason}")
            except:
                messages.error(request,"some error occurred !")
    else:
        fm=LeaveForm()
    return render(request,"staff/staff_leave.html",{'form':fm,'leave_data':leave_data})

@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
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


@csrf_exempt
@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def get_subjects(request):
    data=json.loads(request.body)
    print(data)
    course=data["course"]
    print("course",course)
    course=Courses.objects.get(id=course)
    subjects=Subjects.objects.filter(course=course,staff=request.user.id)
    subjects_data=serializers.serialize("python",subjects)
    subjects_list=[]
    for subject in subjects:
        subject_data={"id":subject.id,"subject_name":subject.subject_name}
        subjects_list.append(subject_data)
    return JsonResponse(json.dumps(subjects_list),content_type="application/json",safe=False)

@csrf_exempt
@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def get_attendance_dates(request):
    data=json.loads(request.body)
    course=data['course']
    subject_id=data['subject']
    session=data['session']
    subject=Subjects.objects.get(id=subject_id)
    session_year=Sessionyearmodel.objects.get(id=session)
    attendance_objects=Attendance.objects.filter(subject_id=subject,session_year=session_year)
    attendance_objects_data=serializers.serialize("python",attendance_objects)
    dates_list=[]
    for obj in attendance_objects:
        date_obj={'id':obj.id,'date':str(obj.attendance_date)}
        dates_list.append(date_obj)
    print(data)
    print(dates_list)
    return JsonResponse(json.dumps(dates_list),content_type="application/json",safe=False)

@csrf_exempt
@login_required(login_url="/")
@checklogindecorator2(allowed_roles=['2'])
def get_attendance_data(request):
    data=json.loads(request.body)
    attendance_id=data['attendance_date_id']
    attendance_obj=Attendance.objects.get(id=attendance_id)
    attendance_objects=AttendanceReport.objects.filter(attendance_id=attendance_obj)
    list_data=[]
    for attendance_data in attendance_objects:
        data_individual={'id':attendance_data.student_id.admin.id,"name":attendance_data.student_id.admin.first_name,"status":attendance_data.status}
        list_data.append(data_individual)
    print(list_data)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)
    
    