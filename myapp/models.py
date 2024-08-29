from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Students must have an email address')
        email = self.normalize_email(email)
        student = self.model(email=email, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

class Student(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class StudentProfile(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.student.email}'

class Professor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    office_location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'Professor {self.first_name} {self.last_name}'

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    course_code = models.CharField(max_length=10, unique=True)
    credits = models.PositiveIntegerField(default=10, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    syllabus = models.FileField(upload_to='syllabi/', blank=True, null=True)
    professors = models.ManyToManyField(Professor)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    classroom_location = models.CharField(max_length=255, blank=True, null=True)
    schedule = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.student.email} - {self.subject.name}: {self.grade}'

    class Meta:
        unique_together = ('student', 'subject',)

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.email} enrolled in {self.course.title} on {self.date_enrolled}'

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NewStudentRegistration(models.Model):
    STUDENT_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    COURSE_CHOICES = (
        ('bsit', 'BSIT'),
        ('cs', 'BSCS'),
        ('bshm', 'BSHM'),
        ('crim', 'BSCRIM'),
        ('bsp', 'BSP'),
        ('bsed', 'BSEd'),
    )

    YEAR_LEVEL_CHOICES = (
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    )

    SEMESTER_CHOICES = (
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    )

    student_type = models.CharField(max_length=50, choices=STUDENT_TYPE_CHOICES)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True)
    student_number = models.CharField(max_length=50, unique=True, blank=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES)
    semester = models.CharField(max_length=50, choices=SEMESTER_CHOICES, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if not self.student_number:
            year = timezone.now().year
            last_student = NewStudentRegistration.objects.filter(student_number__startswith=str(year)).order_by('-student_number').first()
            if last_student:
                last_number = int(last_student.student_number[-5:])
            else:
                last_number = 0
            new_number = f"{year}{str(last_number + 1).zfill(5)}"
            self.student_number = new_number
        super(NewStudentRegistration, self).save(*args, **kwargs)

    def __str__(self):
        return self.student_number
