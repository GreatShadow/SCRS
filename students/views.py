#from pydoc import ModuleScanner
from cgitb import reset
from django.shortcuts import render, redirect

from .forms import StudentLoginForm
from .models import Student, EnrolledCourses, Course

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

        data_dict1 = {}
        search_data1 = request.GET.get('q', "")
        if search_data1:
            if search_data1.isdigit():
                data_dict1["course_number__contains"] = search_data1
            else:
                data_dict1["course_name__contains"] = search_data1

        #courses = Course.objects.get(course_number=erdcourse.course_number.course_number)
        #courses = Course.objects.filter(course_number=erdcourse.course_number.course_number).filter(**data_dict1)

        print(erdcourse.course_number.course_number)
        print(Course.objects.get(course_number=erdcourse.course_number.course_number))
        #print(Course.objects.filter(course_number=erdcourse.course_number.course_number).filter(**data_dict1))

    
    return render(request, 'home.html', {
        'courses': courses#, "search_data": search_data1
    })

def course(request):
    student_number = request.session.get("info")
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        if search_data.isdigit():
            data_dict["course_number__contains"] = search_data
        else:
            data_dict["course_name__contains"] = search_data
    
    #all
    # 
    # class search(View):
    #def get(self,request):
        #chaxungj = request.GET
        #c_d = Course.objects.all().filter(course_name=request.GET["search"])
        #return render(request, 'search.html',{'search':request.GET["search"],'c_d':c_d})
    #def post(self,request):
        #return render(request, 'search.html')
#
    courses_list = Course.objects.all().filter(**data_dict)
    return render(request, 'course.html', {
        'courses': courses_list, "search_data": search_data
    })