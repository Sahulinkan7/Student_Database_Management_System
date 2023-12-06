from django.shortcuts import render 
from .forms import AttendanceCheckForm
from .models import Courses,Subjects,Students,Attendance,AttendanceReport
from django.contrib import messages

def subjectchoicelist(course):
    subjects=Subjects.objects.filter(course=course)
    choice_list=[]
    for i in subjects:
        choice_list.append((i.id,i.subject_name))
    return choice_list


def student_home(request):
    return render(request,"student/student_home.html")

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
    print("st : ",attendance_reports)
    return render(request,"student/my_attendance.html",{'form':fm,'attendance_reports':attendance_reports})