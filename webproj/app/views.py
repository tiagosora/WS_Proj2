from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from app import triplestore

def authentication(request):
    return render(request, 'app/login.html')

# Create your views here.
def wizard_detail(request, wizard_id):
    wizard_data = triplestore.get_wizard_info(wizard_id)

    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

@login_required
def index(request):
    
    return render(request, 'app/index.html')

def student_dashboard(request):
    
    student_info = request.session['student_info']

    student = student_info['student']
    is_learning_courses = student_info['is_learning_courses']
    learned_courses = student_info['learned_courses']
    
    total_number_of_spells = triplestore.get_len_all_spells()
    
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
    
    return render(request, 'app/student_dashboard.html', {
        'student': student,
        'is_learning_courses': is_learning_courses,
        'learned_courses': learned_courses,
        'spells_acquired': spells_acquired,
        'skills': ", ".join(student_info["skills"]),
        'number_of_spells_not_acquired': number_of_spells_not_acquired,
        'spells_per_course': spells_per_course,
        'page_obj': page_obj,
    })

def professor_dashboard(request):
    return render(request, 'app/professor/dashboard.html')

def headmaster_dashboard(request):
    return render(request, 'app/headmaster/dashboard.html')

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

        success = triplestore.create_new_wizard(password, blood_type, eye_color, gender, house, nmec, name, patronus,
                                                species, wand)  # Fill in other parameters
        if success[0]:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = success[1]  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})

    return render(request, 'registration/login.html')

def login_view(request):
    if request.method == 'POST':
        nmec = request.POST.get('id_number')
        password = request.POST.get('password')

        success, id_number = triplestore.login(nmec, password)

        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in
             
            #ver qual o role da pessoa que se autenticou e ir para a pagina correspondente
            wizard_info, _, wizard_type_id = triplestore.get_role_info_by_wizard_id(id_number)
            
            match(wizard_info):
                case 'student': 
                    print("here")
                    request.session['student_info'] = triplestore.get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                case 'profesor':
                    return professor_dashboard(request) #TODO: mudar para pagina do professor
                case 'headmaster':
                    return professor_dashboard(request) #TODO: mudar para pagina do professor
                case _ : 
                    return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # Update 'home_page_url' to your actual home page URL name

