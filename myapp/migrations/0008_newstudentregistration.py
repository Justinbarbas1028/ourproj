# Generated by Django 5.0.4 on 2024-08-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_enrollment_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewStudentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_type', models.CharField(choices=[('new', 'New Student'), ('old', 'Old Student')], max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('student_number', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('course', models.CharField(max_length=100)),
                ('year_level', models.CharField(blank=True, max_length=10, null=True)),
                ('semester', models.CharField(blank=True, max_length=15, null=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
