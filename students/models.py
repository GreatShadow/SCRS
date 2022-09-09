from django.db import models

# Create your models here.
class Student(models.Model):
    student_number = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    current_year = models.CharField(max_length=50)
    field_of_study = models.CharField(max_length=50)
    gpa = models.FloatField()

    def __str__(self):
        return f'Student: {self.first_name} {self.last_name}'

class Course(models.Model):
    course_number = models.PositiveIntegerField(unique=True)
    course_name = models.CharField(max_length=100)
    credit = models.PositiveIntegerField()

class EnrolledCourses(models.Model):
    student_number = models.ForeignKey(to="Student", to_field="student_number", on_delete=models.CASCADE)
    course_number = models.ForeignKey(to="Course", to_field="course_number", on_delete=models.CASCADE)