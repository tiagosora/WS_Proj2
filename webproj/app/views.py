from app.decorators import (headmaster_required, logout_required,
                            professor_required, student_required)
from app.triplestore.courses import (add_spell_to_course,
                                     add_student_to_course,
                                     change_course_professor,
                                     get_course_by_id_dict, get_courses_dict,
                                     remove_spell_from_course,
                                     remove_student_from_course,
                                     update_is_learning_to_learned)
from app.triplestore.professors import (get_all_teachers_not_teaching_course,
                                        get_professor_info)
from app.triplestore.spells import get_len_all_spells
from app.triplestore.students import (get_spells_not_taught_in_course,
                                      get_students_not_learning_course,
                                      students_per_school_year)
from app.triplestore.wizards import (create_new_wizard, get_all_students_info,
                                     get_headmaster_info,
                                     get_role_info_by_wizard_id,
                                     get_student_view_info, update_wizard_info,
                                     wizard_login)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


def authentication(request):
    return render(request, 'app/login.html')


@login_required
def index(request):
    return back_to_dashboard(request)


@student_required
def student_dashboard(request):
    wizard_type_id = request.session['wizard_type_id']
    print(wizard_type_id)
    request.session['student_info'] = get_student_view_info(wizard_type_id)

    student_info = request.session['student_info']

    student = student_info['student']
    is_learning_courses = student_info['is_learning_courses']
    learned_courses = student_info['learned_courses']

    total_number_of_spells = get_len_all_spells()

    spells_per_course = {}
    for course in learned_courses:
        spells_per_course[course["name"]] = len(course["spells"])

    spells_acquired = []
    for course in learned_courses:
        for spell in course["spells"]:
            spells_acquired.append(spell)

    number_of_spells_not_acquired = total_number_of_spells - len(spells_acquired)

    paginator = Paginator(spells_acquired, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    skills = [skill["name"] for skill in student_info["skills"]]

    return render(request, 'app/student_dashboard.html', {
        'student': student,
        'is_learning_courses': is_learning_courses,
        'learned_courses': learned_courses,
        'spells_acquired': spells_acquired,
        'skills': ", ".join(skills),
        'number_of_spells_not_acquired': number_of_spells_not_acquired,
        'spells_per_course': spells_per_course,
        'page_obj': page_obj,
    })


@professor_required
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
    
def points_banners(request):
    request.session['back'] = 'back'
    
    students = get_all_students_info()
    students.sort(key=lambda student: (student["points"], student["name"], student["gender"]), reverse=True)
    return render(request, 'app/points_banners.html', {
        'students': students
    })


@headmaster_required
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
        'students_per_school_year': number_students_per_school_year,
        'spells_per_course': number_spells_per_course,
        'students': students_list,
        'courses': courses_in_list,
    })

def give_points(request):
    pass

def update_wizard(request):
    wizard_id = request.POST.get('wizard_id')
    name = request.POST.get('name')
    blood_type = request.POST.get('blood_type')
    gender = request.POST.get('gender')
    species = request.POST.get('species')
    eye_color = request.POST.get('eye_color')
    patronus = request.POST.get('patronus')
    wand = request.POST.get('wand')

    update_wizard_info(wizard_id, name, gender, blood_type, species, eye_color, patronus, wand)

    return back_to_dashboard(request)


@headmaster_required
def course_view(request):
    course_id = request.POST.get('course_id')
    if not course_id:
        course_id = request.session['course_id']
    request.session['course_id'] = course_id
    request.session['back'] = 'back'

    course_full_info = get_course_by_id_dict(course_id)

    course_full_info['number_students_enrolled'] = len(course_full_info['is_learning'])
    course_full_info['number_spells_taught'] = len(course_full_info['spells'])

    available_professors = get_all_teachers_not_teaching_course(course_full_info['professor_info']['id'])
    available_professors.sort(key=lambda professor: professor['name'])

    return render(request, 'app/course.html', {
        'course': course_full_info,
        'available_students': get_students_not_learning_course(course_id),
        'available_spells': get_spells_not_taught_in_course(course_id),
        'available_professors': available_professors,
    })


@require_http_methods(["POST"])
@headmaster_required
def remove_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    remove_student_from_course(course_id, student_id)

    return redirect("course")


@require_http_methods(["POST"])
@headmaster_required
def add_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    add_student_to_course(course_id, student_id)

    return redirect("course")


@require_http_methods(["POST"])
@headmaster_required
def remove_spell(request):
    spell_id = request.POST.get('spell_id')
    course_id = request.POST.get('course_id')

    remove_spell_from_course(course_id, spell_id)

    return redirect("course")


@require_http_methods(["POST"])
@headmaster_required
def add_spell(request):
    spell_id = request.POST.get('spell_id')
    course_id = request.POST.get('course_id')

    add_spell_to_course(course_id, spell_id)

    return redirect("course")


@require_http_methods(["POST"])
@headmaster_required
def change_professor(request):
    professor_id = request.POST.get('professor_id')
    course_id = request.POST.get('course_id')

    change_course_professor(course_id, professor_id)

    return redirect("course")


@logout_required
def register_view(request):
    if request.method == 'POST':
        nmec = request.POST.get('id_number')
        password = request.POST.get('password')
        blood_type = request.POST.get('blood_type')
        eye_color = request.POST.get('eye_color')
        gender = request.POST.get('gender')
        house = request.POST.get('house')
        name = request.POST.get('name')
        patronus = request.POST.get('patronus')
        species = request.POST.get('species')
        wand = request.POST.get('wand')

        success, id_number = create_new_wizard(password, blood_type, eye_color, gender, house, nmec, name, patronus,
                                               species, wand)
        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number
            request.session['authenticated'] = True

            wizard_role, wizard_type_id = get_role_info_by_wizard_id(id_number)

            match wizard_role:
                case 'student':
                    request.session['student_info'] = get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                case _:
                    logout(request)
                    return redirect("index")

        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})

    return render(request, 'registration/login.html')


@login_required
def back_to_dashboard(request):
    wizard_info = request.session['role']
    request.session['back'] = 'back'
    del request.session['back']
    match wizard_info:
        case 'http://hogwarts.edu/ontology.owl#Student':
            return redirect("student_dashboard")
        case 'http://hogwarts.edu/ontology.owl#Professor':
            return redirect("professor_dashboard")
        case 'http://hogwarts.edu/ontology.owl#Headmaster':
            return redirect("headmaster_dashboard")
        case _:
            logout(request)
            return redirect("index")


@logout_required
def login_view(request):
    if request.method == 'POST':
        nmec = int(request.POST.get('id_number'))
        password = request.POST.get('password')

        success, id_number = wizard_login(nmec, password)

        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number
            request.session['authenticated'] = True

            wizard_role, wizard_type_id = get_role_info_by_wizard_id(id_number)

            print(wizard_role)
            request.session['role'] = wizard_role
            request.session['wizard_type_id'] = wizard_type_id

            match wizard_role:
                case 'http://hogwarts.edu/ontology.owl#Student':
                    return redirect("student_dashboard")
                case 'http://hogwarts.edu/ontology.owl#Professor':
                    return redirect("professor_dashboard")
                case 'http://hogwarts.edu/ontology.owl#Headmaster':
                    return redirect("headmaster_dashboard")
                case _:
                    logout(request)
                    return redirect("index")
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})
    return render(request, 'registration/login.html')


@require_http_methods(["POST"])
@professor_required
def pass_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    update_is_learning_to_learned(course_id, student_id)

    request.session['professor_info'] = get_professor_info(request.session['wizard_type_id'])
    return redirect("professor_dashboard")


@login_required(redirect_field_name="")
def logout_view(request):
    logout(request)
    return redirect('index')
