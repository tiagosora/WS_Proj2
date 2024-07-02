from app.triplestore.courses import get_courses_dict
from app.triplestore.professors import get_professor_info
from app.triplestore.spells import get_len_all_spells
from app.triplestore.students import students_per_school_year
from app.triplestore.wizards import (get_all_students_info,
                                     get_headmaster_info,
                                     get_student_view_info, update_wizard_info)
from django.core.paginator import Paginator
from django.shortcuts import render


def student_dashboard(request):
    wizard_type_id = request.session['wizard_type_id']
    request.session['student_info'] = get_student_view_info(wizard_type_id)

    student_info = request.session['student_info']
    learned_courses = student_info['learned_courses']

    spells_per_course = {}
    for course in learned_courses:
        spells_per_course[course["name"]] = len(course["spells"])

    spells_acquired = []
    for course in learned_courses:
        for spell in course["spells"]:
            spells_acquired.append(spell)

    number_of_spells_not_acquired = get_len_all_spells() - len(spells_acquired)

    paginator = Paginator(spells_acquired, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    skills = [skill["name"] for skill in student_info["skills"]]

    return render(request, 'app/student_dashboard.html', {
        'student': student_info['student'],
        'is_learning_courses': student_info['is_learning_courses'],
        'learned_courses': learned_courses,
        'spells_acquired': spells_acquired,
        'skills': ", ".join(skills),
        'number_of_spells_not_acquired': number_of_spells_not_acquired,
        'spells_per_course': spells_per_course,
        'page_obj': page_obj,
    })


def professor_dashboard(request):
    wizard_type_id = request.session['wizard_type_id']

    request.session['professor_info'] = get_professor_info(wizard_type_id)
    
    students_list = get_all_students_info()
    students_list.sort(key=lambda student: (student["name"], student["gender"], student["blood_type"]))

    professor_info = request.session['professor_info']

    return render(request, 'app/professor_dashboard.html', {
        'professor': professor_info["professor"],
        'courses': professor_info["courses"],
        'students': students_list,
    })


def headmaster_dashboard(request):
    wizard_type_id = request.session['wizard_type_id']

    request.session['headmaster_info'] = get_headmaster_info(wizard_type_id)

    headmaster_info = request.session['headmaster_info']

    students_list = get_all_students_info()
    students_list.sort(key=lambda student: (student["name"], student["gender"], student["blood_type"]))

    courses = get_courses_dict()
    number_spells_per_course = {}
    courses_in_list = []
    for id, course in courses.items():
        course["id"] = id
        course["number_spells_taught"] = len(course["spells"])
        courses_in_list.append(course)

        number_spells_per_course[course["name"]] = len(course["spells"])

    number_students_per_school_year = students_per_school_year()

    courses_in_list.sort(key=lambda course: (course["attending_year"], course["name"]))
    

    return render(request, 'app/headmaster_dashboard.html', {
        'headmaster': headmaster_info,
        'headmaster_id': wizard_type_id,
        'students_per_school_year': number_students_per_school_year,
        'spells_per_course': number_spells_per_course,
        'students': students_list,
        'courses': courses_in_list,
    })


def update_wizard(request):
    wizard_id = request.POST.get('wizard_id')
    name = request.POST.get('name')
    blood_type = request.POST.get('blood_type')
    gender = request.POST.get('gender')
    species = request.POST.get('species')
    eye_color = request.POST.get('eye_color')
    patronus = request.POST.get('patronus')
    wand = request.POST.get('wand')

    update_wizard_info(wizard_id, not request.session.get('infering', True),
                       name, gender, blood_type, species, eye_color, patronus, wand)
