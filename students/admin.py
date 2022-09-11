from django.contrib import admin
from .models import Student, Course, EnrolledCourses

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(EnrolledCourses)