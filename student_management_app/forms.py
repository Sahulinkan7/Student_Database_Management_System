from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms 
from.models import Courses,Staffs,CustomUser,Students,Subjects,Sessionyearmodel

def bring_course():
    try:  
        courses=Courses.objects.all()
        clist=[]
        for c in courses:
            course=(c.id,c.course_name)
            clist.append(course)
        return clist
    except :
        pass
    


def bring_staff():
    try:
        staffs=CustomUser.objects.filter(user_type=2).values('id','first_name')
        staff_list=[]
        try:
            
            for s in staffs:
                staff_list.append(s)
        except :
            pass
        staff_tuple_list=[]
        for st in staff_list:
            val=[val for key,val in st.items()]
            staff_tuple_list.append(tuple(val))
        return staff_tuple_list
    except :
        print("some error")
        
def session_choice():
    sessions=Sessionyearmodel.objects.all()
    ses_list=[]
    for ses in sessions:
        session=(ses.id,str(ses.session_start_year)+"  To  "+str(ses.session_end_year))
        ses_list.append(session)
    return ses_list
    
SESSION_CHOICE=session_choice()
STAFF_CHOICE=bring_staff()
COURSE_CHOICE=bring_course()
GENDER=[('Male','Male'),('Female','Female')]

class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class meta:
        model=User
        fields="__all__"

class AddSessionForm(forms.ModelForm):
    class Meta:
        model=Sessionyearmodel
        fields=['session_start_year','session_end_year']
        widgets={'session_start_year':forms.DateInput(attrs={'class':'form-control','type':'date'}),
                 'session_end_year':forms.DateInput(attrs={'class':'form-control','type':'date'})}
        
class AddstaffForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    
class AddCourseForm(forms.ModelForm):
    course_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':'Enter course name'})))
    class Meta:
        model=Courses
        fields=['course_name']
        
class AddStudentForm(forms.Form):
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}))
    course=forms.ChoiceField(choices=COURSE_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    gender=forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class':'form-control'}))
    session_year=forms.ChoiceField(choices=SESSION_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    address=forms.CharField(max_length=255,widget=forms.Textarea(attrs={'class':'form-control'}))
    
    
class AddSubjectForm(forms.Form):
    subject_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    course=forms.ChoiceField(choices=COURSE_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    staff=forms.ChoiceField(choices=STAFF_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    
    
class EditStaffForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email']
        
        
class EditStudentForm(forms.ModelForm):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'})) 
    session_year=forms.ChoiceField(choices=SESSION_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    course=forms.ChoiceField(choices=COURSE_CHOICE,widget=forms.Select(attrs={'class':'form-control'}))
    gender=forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class':'form-control'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','username']
        
class EditCourseForm(forms.ModelForm):
    class Meta:
        model=Courses
        fields=['course_name']
        widgets={'course_name':forms.TextInput(attrs={'class':'form-control'})}
        
class EditSubjectForm(forms.ModelForm):
    class Meta:
        model=Subjects
        fields=['subject_name','course']
        widgets={'subject_name':forms.TextInput(attrs={'class':'form-control'}),
                 'course':forms.Select(attrs={'class':'form-control'})}
        
class LeaveForm(forms.Form):
    date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    reason=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    
    
    
class FeedbackForm(forms.Form):
    feedback_message=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))