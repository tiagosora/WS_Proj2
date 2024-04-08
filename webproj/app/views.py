from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def authentication(request):
    return render(request, 'app/login.html')

#### DEVELOPMENT ####
from app import triplestore


# Create your views here.
def wizard_detail(request, wizard_id):
    wizard_data = triplestore.get_wizard_info(wizard_id)

    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

@login_required
def index(request):
    
    return render(request, 'app/index.html')

# def student_dashboard(request):
    
#     # Mock Student
#     student = {
#         "name": "Sirius Black",
#         "species": "Human",
#         "blood_type": "Pure-blood",
#         "gender": "Male",
#         "house": "Gryffindor",
#         "school": "Hogwarts",
#         "school_year": 1,
#         "skills": ["Animagus (Dog)", "Defensive Magic"],
#         "patronus": "Non-corporeal",
#         "wand": None,
#         "eye_color": "Grey",
#     }

#     # Mock Course
#     courses = [
#         {
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         },{
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         },{
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         },{
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         },{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
#         ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
#         ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
#         ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
#         ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] },{
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         },{
#         "name": "Defence Against the Dark Arts",
#         "professor_in_charge": "Remus Lupin",
#         "spells_taught": [
#             {
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "Expecto Patronum",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },{
#                 "name": "dwdwdw",
#                 "incantation": "Expecto Patronum",
#                 "effect": "Summons a Patronus",
#                 "light": "Silver",
#                 "type": "Charm"
#             },
#             ]
#         }
#     ]
    
#     spells = []
#     for course in courses:
#         spells_taught = course["spells_taught"]
#         for spell in spells_taught:
#             spells.append(spell)
            
#     print(len(spells))
            
#     paginator = Paginator(spells, 24)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     spells_per_course = {'Potions': 5, 'Charms': 3, 'Transfiguration': 2}


#     return render(request, 'app/student_dashboard.html', {
#         'student': student,
#         'is_learning_courses': courses,
#         'learned_courses': courses,
#         'spells_acquired': spells,
#         'skills': ", ".join(student["skills"]),
#         'n_spells_not_acquired': 10,
#         'spells_per_course': spells_per_course,
#         'page_obj': page_obj,
#     })

def student_dashboard(request):

    
    
    unique_spells = []
    for course in courses:
        spells_taught = course["spells_taught"]
        for spell in spells_taught:
            spells.append(spell)
            
    print(len(spells))
            
    paginator = Paginator(spells, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    spells_per_course = {'Potions': 5, 'Charms': 3, 'Transfiguration': 2}


    return render(request, 'app/student_dashboard.html', {
        'student': student,
        'is_learning_courses': courses,
        'learned_courses': courses,
        'spells_acquired': spells,
        'skills': ", ".join(student["skills"]),
        'n_spells_not_acquired': 10,
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
    print(request)
    if request.method == 'POST':
        nmec = request.POST.get('id_number')
        password = request.POST.get('password')

        success, id_number = triplestore.login(nmec, password)

        print(success)

        if success[0]:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in
             
            #ver qual o role da pessoa que se autenticou e ir para a pagina correspondente
            wizard_info, wizard_role, wizard_type_id = triplestore.get_role_info_by_wizard_id(id_number)
            
            print(wizard_role)
            
            match(wizard_role):
                case 'student': 
                    request.session['student_info'] = triplestore.get_student_view_info(wizard_type_id)
                    redirect('app/student_dashboard.html')
                case 'profesor':
                    redirect('index') #TODO: mudar para pagina do professor
                case 'headmaster':
                    redirect('index') #TODO: mudar para pagina do professor
                case _ : 
                    return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # Update 'home_page_url' to your actual home page URL name

