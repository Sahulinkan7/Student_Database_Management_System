from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import (Staffs,Students,Subjects,Sessionyearmodel,Attendance,AttendanceReport,LeaveReportStaff,
                    LeaveReportStudent)

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Sessionyearmodel)
admin.site.register(AttendanceReport)
admin.site.register(Attendance)
admin.site.register(LeaveReportStaff)
admin.site.register(LeaveReportStudent)