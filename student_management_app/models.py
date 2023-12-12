from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    
class Sessionyearmodel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    
class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    def __str__(self):
        return self.admin.first_name+" "+self.admin.last_name
    
    class Meta:
        verbose_name_plural='Staffs'
    
class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    def __str__(self):
        return self.course_name
    
    class meta:
        verbose_plural_name='Courses'
    
class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    staff=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    
    def __str__(self):
        return self.subject_name
    
    class Meta:
        verbose_name_plural='Subjects'
    
class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,default=1)
    session_year=models.ForeignKey(Sessionyearmodel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    def __str__(self) -> str:
        return self.admin.first_name+" "+self.admin.last_name
    
    class Meta:
        verbose_name_plural='Students'
    
class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    session_year=models.ForeignKey(Sessionyearmodel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    class Meta:
        verbose_name_plural='Attendance'
    
class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
    def __str__(self) -> str:
        return str(self.attendance_id.attendance_date)+" "+str(self.student_id.admin.first_name)+str(self.attendance_id.subject_id.subject_name)+" "+str(self.status)
    
class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.DateField()
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class LeaveReportStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    leave_date=models.DateField()
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    

class FeedbackStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
        
        
class FeedbackStaffs(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class NotificationStudents(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
        
    
class NotificationStaffs(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class Examination(models.Model):
    id=models.AutoField(primary_key=True)
    exam_name=models.CharField(unique=True,max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class CourseExam(models.Model):
    id=models.AutoField(primary_key=True)
    exam=models.ForeignKey(Examination,on_delete=models.DO_NOTHING)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    session=models.ForeignKey(Sessionyearmodel,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
class ExamResult(models.Model):
    id=models.AutoField(primary_key=True)
    course_exam=models.ForeignKey(CourseExam,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE,default="")
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    subject_exam_mark=models.FloatField(default=0)
    subject_assignment_mark=models.FloatField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance,course=Courses.objects.get(id=1),session_year=Sessionyearmodel.objects.get(id=1))
            
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()