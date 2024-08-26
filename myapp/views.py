from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, LoginForm, StudentEditForm, ChangePasswordForm, ProfessorForm, StudentProfileForm, CourseForm, SubjectForm, AnnouncementForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Student, StudentProfile, Course, Subject, Professor, Announcement

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_admin:
                        return redirect('home')
                    else:
                        return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])
            student.save()
            return redirect('register')
    else:
        form = StudentRegistrationForm()
    return render(request, 'pages/register.html', {'form': form})

def index(request):
    return render(request, 'pages/index.html')


def landingpage(request):
    return render(request, 'pages/landingpage.html')

def registration(request):
    return render(request, 'pages/registration.html')

@login_required
def administrator_page(request):
    if not request.user.is_admin:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'pages/administrator_page.html')

@login_required
def home(request):
    return render(request, 'pages/homepage.html')

@login_required
def about(request):
    return render(request, 'pages/about.html')

@login_required
def courses(request):
    return render(request, 'pages/courses.html')

@login_required
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'pages/subjects.html', {'subjects': subjects})

@login_required
def announcement(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'pages/announcement.html', {'announcements': announcements})

@login_required
def add_announcement(request):
    if not request.user.is_admin:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement')
    else:
        form = AnnouncementForm()
    return render(request, 'pages/add_announcement.html', {'form': form})

@login_required
def update_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'pages/update_announcement.html', {'form': form, 'announcement': announcement})

@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement')
    return render(request, 'pages/delete_announcement.html', {'announcement': announcement})

@login_required
def profile(request):
    return render(request, 'pages/profile.html')

@login_required
def admin_student_list(request):
    students = Student.objects.all()
    return render(request, 'pages/admin_student_list.html', {'students': students})

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'pages/administrator_page.html')

@login_required
def student_dashboard(request):
    if request.user.is_admin:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'pages/home.html')


@login_required
def admin_edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_profile, created = StudentProfile.objects.get_or_create(student=student)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            if 'profile_picture' in request.FILES:
                student_profile.profile_picture = request.FILES['profile_picture']
                student_profile.save()
            return redirect('admin_student_list')
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'pages/admin_edit_student.html', {'form': form, 'student': student})
@login_required
def admin_delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('admin_student_list')
    return render(request, 'pages/admin_delete_student.html', {'student': student})

@login_required
def change_password(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if student.check_password(cd['old_password']):
                student.set_password(cd['new_password'])
                student.save()
                update_session_auth_hash(request, student)
                return redirect('admin_student_list')
            else:
                form.add_error('old_password', 'Old password is incorrect')
    else:
        form = ChangePasswordForm()
    return render(request, 'pages/change_password.html', {'form': form, 'student': student})



def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def profile(request):
    student = request.user
    student_profile, created = StudentProfile.objects.get_or_create(student=student)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile = profile_form.save(commit=False)
            profile.student = student
            profile.save()
            return redirect('profile')
    else:
        form = StudentEditForm(instance=student)
        profile_form = StudentProfileForm(instance=student_profile)

    return render(request, 'pages/profile.html', {'student': student, 'student_profile': student_profile, 'form': form, 'profile_form': profile_form})

@login_required
def profile_update(request):
    student = request.user
    student_profile, created = StudentProfile.objects.get_or_create(student=student)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('profile')
    else:
        form = StudentEditForm(instance=student)
        profile_form = StudentProfileForm(instance=student_profile)

    return render(request, 'pages/profile_form.html', {'form': form, 'profile_form': profile_form})

@login_required
def professors_list(request):
    professors = Professor.objects.all()
    return render(request, 'pages/professors_list.html', {'professors': professors})

def add_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_professor')
    else:
        form = ProfessorForm()
    return render(request, 'pages/add_professor.html', {'form': form})

@login_required
def update_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('professors_list')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'pages/update_professor.html', {'form': form, 'professor': professor})
@login_required
def delete_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    if request.method == 'POST':
        professor.delete()
        return redirect('add_professor')
    return render(request, 'pages/delete_professor.html', {'professor': professor})

@login_required
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'pages/courses_list.html', {'courses': courses})

@login_required
def add_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'pages/add_courses.html', {'form': form})

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'pages/update_courses.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')
    return render(request, 'pages/delete_course.html', {'course': course})

@login_required
def subjects_list(request):
    subjects = Subject.objects.all()
    return render(request, 'pages/subjects_list.html', {'subjects': subjects})

@login_required
def add_subjects(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects_list')
    else:
        form = SubjectForm()
    return render(request, 'pages/add_subjects.html', {'form': form})

@login_required
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subjects_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'pages/update_subject.html', {'form': form, 'subject': subject})

@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        return redirect('subjects_list')
    return render(request, 'pages/delete_subject.html', {'subject': subject})

