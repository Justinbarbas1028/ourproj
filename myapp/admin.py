from django.contrib import admin
from .models import Student, StudentProfile, Professor, Course, Subject, Enrollment, Announcement, Grade

class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'phone_number', 'address')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'phone_number', 'address')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email', 'department')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    filter_horizontal = ('professors',)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'professor')
    search_fields = ('name', 'course__title', 'professor__first_name', 'professor__last_name')


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    search_fields = ('student__email', 'course__title')
    readonly_fields = ('date_enrolled',)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade')
    search_fields = ('student', 'subject', 'grade')

admin.site.register(Student, StudentAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Grade, GradeAdmin)