from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect

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

def toggle_infering(request):
    if 'infering' in request.session:
        request.session['infering'] = not request.session['infering']
    else:
        request.session['infering'] = True
    return JsonResponse({'infering': request.session['infering']})

def initialize_infering(request):
    if 'infering' not in request.session:
        request.session['infering'] = True
    return JsonResponse({'infering': request.session['infering']})
