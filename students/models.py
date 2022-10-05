from pyexpat import model
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

    # preferences of a student, [0, 10]
    interested_in_math = models.FloatField(default=0.0)
    interested_in_cs = models.FloatField(default=0.0)
    interested_in_art = models.FloatField(default=0.0)
    interested_in_history = models.FloatField(default=0.0)
    interested_in_literature = models.FloatField(default=0.0)
    interested_in_law = models.FloatField(default=0.0)
    interested_in_philosophy = models.FloatField(default=0.0)
    interested_in_pedagogy = models.FloatField(default=0.0)

    mocked = models.BooleanField(default=False)

    def __str__(self):
        return f'Student: {self.first_name} {self.last_name}'

class Course(models.Model):
    course_number = models.PositiveIntegerField(unique=True)
    course_name = models.CharField(max_length=100)
    course_field = models.CharField(max_length=100, default="")
    
    # features of a course, assume [1, 5]
    credit = models.PositiveIntegerField()

    # percentage of students taking this course
    selected_ratio = models.FloatField(default=0.0)

    # Course Difficulty (between 1 and 10)
    difficulty = models.FloatField(default=0.0)

    # percentage of students who pass this course
    passed_ratio = models.FloatField(default=0.0)

    # Students' ratings for this class (between 1 and 10)
    satisfaction = models.FloatField(default=0.0)
    
    mocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.course_name


class EnrolledCourses(models.Model):
    student_number = models.ForeignKey(to="Student", to_field="student_number", on_delete=models.CASCADE)
    course_number = models.ForeignKey(to="Course", to_field="course_number", on_delete=models.CASCADE)
    mocked = models.BooleanField(default=False)
