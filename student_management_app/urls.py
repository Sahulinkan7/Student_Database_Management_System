from django.urls import path
from . import views,adminviews,staff_views,student_views

urlpatterns = [
    path("",views.login_view,name="login_view"),
    path("dashboard_view/",views.dashboard_view,name="dashboard_view"),
    path("addstudent/",adminviews.add_student_view,name="add_student"),
    path("manage_students/",adminviews.manage_students_view.as_view(),name="manage_students"),
    path("edit_student/<int:pk>/",adminviews.edit_student_view,name="edit_student"),
    path("addstaff/",adminviews.add_staff_view,name="add_staff"),
    path("manage_staffs/",adminviews.manage_staffs_view.as_view(),name="manage_staffs"),
    path("edit_staff/<int:staff_id>/",adminviews.edit_staff_view,name="edit_staff"),
    path("addcourse/",adminviews.add_course_view,name="add_course"),
    path("manage_courses/",adminviews.manage_courses_view.as_view(),name="manage_courses"),
    path("edit_course/<int:course_id>/",adminviews.edit_course_view,name="edit_course"),
    path("addsubject/",adminviews.add_subject_view,name="add_subject"),
    path("manage_subjects/",adminviews.manage_subjects_view.as_view(),name="manage_subjects"),
    path("edit_subject/<int:subject_id>/",adminviews.edit_subject_view,name="edit_subject"),
    path("manage_sessions/",adminviews.manage_session_view.as_view(),name="manage_sessions"),
    path("take_student_attendance/",staff_views.take_attendance,name="take_student_attendance"),
    path("get_students/",staff_views.get_students,name="get_students"),
    path("save_student_attendance/",staff_views.save_attendance_data,name="save_student_attendance"),
    path("staff_leave_apply",staff_views.staff_leave,name="staff_leave_apply"),
    path("staff_feedback/",staff_views.staff_feedback,name="staff_feedback"),
    path("view_my_attendance/",student_views.show_my_attendance,name="student_view_attendance"),
    path("logout/",views.logout_view,name="logout"),
]
