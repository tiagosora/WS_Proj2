from django.contrib.auth import logout
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
