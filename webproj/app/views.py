from app.decorators import student_required, professor_required, headmaster_required, logout_required
from app.triplestore.courses import update_is_learning_to_learned, get_courses_dict
from app.triplestore.professors import get_professor_info
from app.triplestore.spells import get_len_all_spells
from app.triplestore.students import students_per_school_year
from app.triplestore.wizards import get_role_info_by_wizard_id, get_headmaster_info, get_student_view_info, wizard_login, create_new_wizard
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

def authentication(request):
    return render(request, 'app/login.html')

# Create your views here.

@login_required
def index(request):
    return render(request, 'app/index.html')


@student_required
def student_dashboard(request):
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
    professor_info = request.session['professor_info']
    return render(request, 'app/professor_dashboard.html', {
        'professor': professor_info["professor"],
        'courses': professor_info["courses"],
    })


@headmaster_required
def headmaster_dashboard(request):
    headmaster_info = request.session['headmaster_info']
    print(headmaster_dashboard)
    print()
    print(students_per_school_year())
    print()
    courses_dict = get_courses_dict()
    print(courses_dict)
    
    return render(request, 'app/headmaster_dashboard.html', {
        'headmaster': headmaster_info,
        'students_per_school_year': students_per_school_year(),
        'courses_dict': courses_dict,
    })


@logout_required
def register_view(request):
    if request.method == 'POST':
        # Here you would retrieve form data
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

        # For example, using your create_new_wizard function

        success, id_number = create_new_wizard(password, blood_type, eye_color, gender, house, nmec, name, patronus,
                                    species, wand)  # Fill in other parameters
        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in

            wizard_info, _, wizard_type_id = get_role_info_by_wizard_id(id_number)

            match wizard_info:
                case 'student':
                    request.session['student_info'] = get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                # case 'profesor':
                #     return professor_dashboard(request)  # TODO: mudar para pagina do professor
                # case 'headmaster':
                #     return professor_dashboard(request)  # TODO: mudar para pagina do professor
                case _:
                    logout(request)
                    return redirect("index")

        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})

    return render(request, 'registration/login.html')


@logout_required
def login_view(request):
    if request.method == 'POST':
        nmec = request.POST.get('id_number')
        password = request.POST.get('password')

        success, id_number = wizard_login(nmec, password)

        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in

            # ver qual o role da pessoa que se autenticou e ir para a pagina correspondente
            wizard_info, _, wizard_type_id = get_role_info_by_wizard_id(id_number)

            request.session['role'] = wizard_info
            request.session['wizard_type_id'] = wizard_type_id
            
            print(wizard_info)
            
            match wizard_info:
                case 'student':
                    request.session['student_info'] = get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                case 'professor':
                    request.session['professor_info'] = get_professor_info(wizard_type_id)
                    return redirect("professor_dashboard")
                case 'headmaster':
                    request.session['headmaster_info'] = get_headmaster_info(wizard_type_id)
                    return redirect("headmaster_dashboard")
                case _:
                    logout(request)
                    return redirect("index")
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})
    return render(request, 'registration/login.html')

@require_http_methods(["POST"])
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
