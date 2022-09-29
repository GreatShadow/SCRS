from django.shortcuts import render, redirect

from .forms import StudentLoginForm
from .models import Student, EnrolledCourses, Course
from django.views import View
# Create your views here.
def index(request):
    if request.method == "GET":
        form = StudentLoginForm()
        return render(request, 'index.html', {'form':form})

    form = StudentLoginForm(request.POST)
    if form.is_valid():
        student_object = Student.objects.filter(**form.cleaned_data).first()
        if not student_object:
            form.add_error("password", "Password is wrong or account is not existing")
            return render(request, 'index.html', {'form':form})
        request.session["info"] = student_object.student_number
        return redirect('/home/')
    return render(request, 'index.html', {'form':form})

def home(request):
    student_number = request.session.get("info")
    erdcourses = EnrolledCourses.objects.filter(student_number=student_number)
    courses = list()
    for erdcourse in erdcourses:
        courses.append(Course.objects.get(course_number=erdcourse.course_number.course_number))
        print(erdcourse.course_number.course_number)
        print(Course.objects.get(course_number=erdcourse.course_number.course_number))
    return render(request, 'home.html', {
        'courses': courses
    })

def course(request):
    courses = Course.objects.all()
    return render(request, 'course.html', {
        'courses': courses})

class search(View):
    def get(self,request):
        chaxungj = request.GET
        c_d = Course.objects.all().filter(course_name=request.GET["search"])
        return render(request, 'search.html',{'search':request.GET["search"],'c_d':c_d})
    def post(self,request):
        return render(request, 'search.html')
