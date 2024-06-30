# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('subjects/', views.subjects, name='subjects'),
    path('courses/', views.courses, name='courses'),
    path('announcement/', views.announcement, name='announcement'),
    path('announcements/add/', views.add_announcement, name='add_announcement'),
    path('announcements/update/<int:announcement_id>/', views.update_announcement, name='update_announcement'),
    path('announcements/delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('administrator_page/', views.administrator_page, name='administrator_page'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_student_list/', views.admin_student_list, name='admin_student_list'),
    path('students/edit/<int:student_id>/', views.admin_edit_student, name='admin_edit_student'),
    path('students/delete/<int:student_id>/', views.admin_delete_student, name='admin_delete_student'),
    path('students/change_password/<int:student_id>/', views.change_password, name='change_password'),
    path('add_professor/', views.add_professor, name='add_professor'),
    path('professor_list/', views.professors_list, name='professors_list'),
    path('professors/update/<int:professor_id>/', views.update_professor, name='update_professor'),
    path('professors/delete/<int:professor_id>/', views.delete_professor, name='delete_professor'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('add_courses/', views.add_courses, name='add_courses'),
    path('course_list/', views.courses_list, name='courses_list'),
    path('courses/update/<int:course_id>/', views.update_course, name='update_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add_subjects/', views.add_subjects, name='add_subjects'),
    path('subject_list/', views.subjects_list, name='subjects_list'),
    path('subjects/update/<int:subject_id>/', views.update_subject, name='update_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

