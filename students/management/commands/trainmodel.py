from ast import Delete
import json
import random
from select import select
from unittest import mock
from django.core.management.base import BaseCommand, CommandError
import math
from students.models import Student, Course, EnrolledCourses


class Command(BaseCommand):
    help = 'train model'

    def add_arguments(self, parser):
        parser.add_argument('--action', type=str, required=True, help="mock_data|train_model")

    def handle(self, *args, **options):
        if options['action'] == 'mock_data':
            self.mock_data()
        elif options['action'] == 'train_model':
            self.train_model()
        else:
            print("invalid action")

    def mock_data(self):
        # clear all mock data
        Course.objects.filter(mocked=True).delete()
        Student.objects.filter(mocked=True).delete()
        EnrolledCourses.objects.filter(mocked=True).delete()
        print("clear all mocked course")

        # generate 100 course
        for course_number in range(1, 101):
            course = Course()
            course.course_number = course_number
            course.course_name = f'CS{course_number}'
            print(f'ganerate course {course.course_name}')
            course.credit = random.randint(1, 5)
            course.selected_ratio = random.randint(20, 90) / 100.0
            course.difficulty = random.randint(10, 100) / 100.0
            course.passed_ratio = 1 - course.difficulty * (random.randint(30, 60) / 100.0)
            if course.passed_ratio < 0 or course.passed_ratio > 1.0:
                course.passed_ratio = 0.65
            
            course.satisfaction = random.randint(40, 100) / 100.0
            course.mocked = True
            course.save()

        # generate 3000 students
        for student_number in range(10000, 13001):
            student = Student()
            student.student_number = student_number
            student.first_name = 'stu'
            student.last_name = f'{student.student_number}'
            student.email = f'stu{student.student_number}@student.uts.edu.au'
            student.password = f'123456'
            student.current_year = '2022'
            student.field_of_study = ''
            student.gpa = random.randint(200, 400) / 100.0
            student.grade = random.randint(1, 4)
            student.credits = random.randint(10, 60)
            student.age = random.randint(16, 22)

            student.mocked = True
            student.save()

            print(f'generate student {student}')

        # generate Enrolled course, each student will select 5~15 courses
        courses = Course.objects.filter(mocked=True)
        for student in Student.objects.filter(mocked=True):
            for _ in range(15, 30):
                enrolled_courses = EnrolledCourses()
                enrolled_courses.student_number = student
                course = random.choice(courses)
                if EnrolledCourses.objects.filter(student_number=student, course_number=course).count() > 0:
                    continue

                enrolled_courses.course_number = course
                enrolled_courses.mocked = True
                enrolled_courses.save()
                print(f'generate {student}-{course}')



    def train_model(self):
        # get the most enrolled courses
        enrolled_course_count = dict()
        for enrolled_course in EnrolledCourses.objects.all():
            course_name = enrolled_course.course_number
            enrolled_course_count[course_name] = enrolled_course_count.get(course_name, 0) + 1

        sorted_items = sorted(enrolled_course_count.items(), key=lambda x: x[1], reverse=True)
        seed_course = sorted_items[0][0]

        def course_to_vector(course):
            # build vector with credit, selected_ratio, difficulty, passed_ratio, satisfaction with nomalization
            return [course.credit / 5, course.selected_ratio, course.difficulty, course.passed_ratio, course.satisfaction / 10]

        def calc_distance(vector_a, vector_b):
            return math.sqrt(sum([(a - b)**2 for (a,b) in zip(vector_a, vector_b)]))

        # generate featur vector of a course
        seed_course_vector = course_to_vector(seed_course)
        N = 20
        course_similarity = dict()
        for course in Course.objects.filter(mocked=True):
            if course.course_number == seed_course.course_number:
                continue

            # calculate similarity between course and seed_course
            course_similarity[course.course_name] = 1 - calc_distance(seed_course_vector, course_to_vector(course))

        sorted_course_items = sorted(course_similarity.items(), key=lambda x: x[1], reverse=True)
        
        select_courses = []
        for index, item in enumerate(sorted_course_items):
            if index >= N:
                break

            select_courses.append(item[0])

        # build vector for all students with the selected courses
        student_course_vectors = dict()
        for student in Student.objects.all():
            student_vector = []
            for course_name in select_courses:
                enrolled_courses_count = EnrolledCourses.objects.filter(student_number=student, course_number__course_name=course_name).count()
                if enrolled_courses_count == 0:
                    student_vector.append(0)
                else:
                    student_vector.append(1)

            student_course_vectors[student.student_number] = student_vector

        # save student vectors for predict
        json.dump(select_courses, open("select_courses.json", "w+"), indent=True)
        json.dump(student_course_vectors, open("student_course_vectors.json", "w+"), indent=True)

        # build vector for all students with their own features
        def student_to_vector(student):
            # normal features
            return [student.gpa / 4.0, student.age / 100.0, student.grade / 4, student.credits / 100]


        student_feature_vectors = dict()
        for student in Student.objects.all():
            student_feature_vectors[student.student_number] = student_to_vector(student)
        
        json.dump(student_feature_vectors, open("student_feature_vectors.json", "w+"), indent=True)

