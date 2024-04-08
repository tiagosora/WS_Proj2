from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def authentication(request):
    return render(request, 'app/authentication.html')

#### DEVELOPMENT ####

@login_required
def index(request):
    return render(request, 'app/index.html')

def student_dashboard(request):
    
    # Mock Student
    student = {
        "name": "Sirius Black",
        "species": "Human",
        "blood_type": "Pure-blood",
        "gender": "Male",
        "house": "Gryffindor",
        "school": "Hogwarts",
        "school_year": 1,
        "skills": ["Animagus (Dog)", "Defensive Magic"],
        "patronus": "Non-corporeal",
        "wand": None,
        "eye_color": "Grey",
    }

    # Mock Course
    courses = [
        {
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        },{
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        },{
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        },{
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        },{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
        ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
        ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
        ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] }
        ,{ "name": "Defence Against the Dark Arts", "professor_in_charge": "Remus Lupin", "spells_taught": [ { "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" },{ "name": "Expecto Patronum", "incantation": "Expecto Patronum", "effect": "Summons a Patronus", "light": "Silver", "type": "Charm" }, ] },{
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        },{
        "name": "Defence Against the Dark Arts",
        "professor_in_charge": "Remus Lupin",
        "spells_taught": [
            {
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "Expecto Patronum",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },{
                "name": "dwdwdw",
                "incantation": "Expecto Patronum",
                "effect": "Summons a Patronus",
                "light": "Silver",
                "type": "Charm"
            },
            ]
        }
    ]
    
    spells = []
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

#### DEVELOPMENT ####

# @login_required
# def dashboard(request):
#     user_role = request.user.role
#     if user_role == 'student':
#         return redirect('student_dashboard')
#     elif user_role == 'professor':
#         return redirect('professor_dashboard')
#     elif user_role == 'headmaster':
#         return redirect('headmaster_dashboard')
#     else:
#         return render(request, 'unauthorized.html')

# @login_required
# def student_dashboard(request):
#     if request.user.type != 'student':
#         return redirect('dashboard')
#     return render(request, 'student/dashboard.html')

# @login_required
# def professor_dashboard(request):
#     if request.user.type != 'professor':
#         return redirect('dashboard')
#     return render(request, 'professor/dashboard.html')

# @login_required
# def headmaster_dashboard(request):
#     if request.user.type != 'headmaster':
#         return redirect('dashboard')
#     return render(request, 'headmaster/dashboard.html')
