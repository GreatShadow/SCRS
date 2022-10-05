import json
import math
from django.shortcuts import render, redirect

from .forms import StudentLoginForm, StudentForm
from SCRS.settings import K, RECOMMENDATION_THRESHOLD

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
        print(erdcourse.course_number.course_number)
        print(Course.objects.get(course_number=erdcourse.course_number.course_number))
    return render(request, 'home.html', {
        'courses': courses
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
    courses_list = Course.objects.all().filter(**data_dict)
    return render(request, 'course.html', {
        'courses': courses_list, "search_data": search_data
    })

def runoob(request):
    return render(request,'about.html')
    
def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student_number = form.cleaned_data['student_number']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            new_current_year = form.cleaned_data['current_year']
            new_field_of_study = form.cleaned_data['field_of_study']
            new_gpa = form.cleaned_data['gpa']

            new_student = Student(
                student_number = new_student_number,
                first_name = new_first_name,
                last_name = new_last_name,
                email = new_email,
                password = new_password,
                current_year = new_current_year,
                field_of_study = new_field_of_study,
                gpa = new_gpa
            )
            new_student.save()
            return render(request, 'register.html', {
                'form': StudentForm(),
                'success': 'True'
            })
    else:
        form = StudentForm()
    return render(request, 'register.html', {
        'form': StudentForm()
    })

    

def recommendation(request):
    student_number = request.session.get("info")

    # load models
    select_courses = json.load(open("models/select_courses.json"))
    student_course_vectors = json.load(open("models/student_course_vectors.json"))
    student_preferences_vectors = json.load(open("models/student_preferences_vectors.json"))

    def student_to_vector(student):
        # normal features
        return [
            student.interested_in_math / 10,
            student.interested_in_cs / 10,
            student.interested_in_art / 10,
            student.interested_in_history / 10,
            student.interested_in_literature / 10,
            student.interested_in_law / 10,
            student.interested_in_philosophy / 10,
            student.interested_in_pedagogy / 10,
        ]

    def calc_distance(vector_a, vector_b):
        return math.sqrt(sum([(a - b)**2 for (a,b) in zip(vector_a, vector_b)]))

    student = Student.objects.get(student_number=student_number)
    student_preferences_vector = student_to_vector(student)

    # calculate similarity with other students
    student_similarities = dict()
    for other_student_number in student_preferences_vectors:
        if other_student_number == student_number:
            continue

        student_similarities[other_student_number] = 1 - calc_distance(student_preferences_vector, student_preferences_vectors[other_student_number])

    # get the most K similar students this current student
    average_course_vectors = [0] * len(select_courses)
    for candicate_student_number, _ in sorted(student_similarities.items(), key=lambda x: x[1], reverse=True)[: K]:
        for index in range(len(select_courses)):
            average_course_vectors[index] += student_course_vectors[candicate_student_number][index]

    recommendations = []
    for index in range(len(select_courses)):
        average_course_vectors[index] /= K
        if average_course_vectors[index] > RECOMMENDATION_THRESHOLD:
            course = Course.objects.get(course_name=select_courses[index])
            recommendations.append(course)

    return render(request, 'recommendations.html', {
        'courses': recommendations
    })
