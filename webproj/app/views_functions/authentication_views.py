from app.triplestore.wizards import (create_new_wizard,
                                     get_role_info_by_wizard_id,
                                     get_student_view_info, wizard_login)
from django.contrib.auth import logout
from django.shortcuts import redirect, render


def authentication(request):
    return render(request, 'app/login.html')

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

def logout_view(request):
    logout(request)
    return redirect('index')
