from django import forms
from .models import Student, StudentProfile, Professor, Course, Subject, Announcement, Grade, NewStudentRegistration

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class StudentEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].initial = self.instance.studentprofile.profile_picture if hasattr(self.instance, 'studentprofile') else None

    def save(self, commit=True):
        student = super().save(commit)
        if 'profile_picture' in self.cleaned_data:
            if hasattr(student, 'studentprofile'):
                student.studentprofile.profile_picture = self.cleaned_data['profile_picture']
                student.studentprofile.save()
            else:
                StudentProfile.objects.create(student=student, profile_picture=self.cleaned_data['profile_picture'])
        return student

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['new_password'] != cd['new_password2']:
            raise forms.ValidationError('New passwords don\'t match.')
        return cd['new_password2']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'email', 'department', 'bio', 'office_location', 'phone_number', 'profile_picture']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['address', 'phone_number', 'profile_picture']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_code', 'credits', 'start_date', 'end_date', 'professors', 'syllabus']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'course', 'professor', 'classroom_location', 'schedule']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade']

class NewStudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    middle_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Middle Name (Optional)'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}))
    address = forms.CharField(max_length=255, required=True, widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Address'}))
    course = forms.ChoiceField(choices=NewStudentRegistration.COURSE_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Select Course'}))
    year_level = forms.ChoiceField(choices=NewStudentRegistration.YEAR_LEVEL_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Select Year Level'}))
    semester = forms.ChoiceField(choices=NewStudentRegistration.SEMESTER_CHOICES, required=False, widget=forms.Select(attrs={'placeholder': 'Select Semester'}))
    age = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'Age'}))
    gender = forms.ChoiceField(choices=NewStudentRegistration.GENDER_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Select Gender'}))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = NewStudentRegistration
        exclude = ['student_number']

class EditStudentForm(forms.ModelForm):
    class Meta:
        model = NewStudentRegistration
        fields = [
            'first_name', 'middle_name', 'last_name', 'student_number',
            'date_of_birth', 'address', 'course', 'year_level',
            'semester', 'age', 'gender', 'contact_number', 'email'
        ]
