# Generated by Django 5.0.4 on 2024-06-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_course_professor_enrollment_course_students_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
