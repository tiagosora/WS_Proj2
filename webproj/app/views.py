from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.triplestore.wizards import create_new_wizard
from app.triplestore.wizards import wizard_login


# Create your views here.

@login_required
def index(request):
    return render(request, 'app/index.html')


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

        success = create_new_wizard(password, blood_type, eye_color, gender, house, nmec, name, patronus,
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

        success = wizard_login(nmec, password)

        print(success)

        if success[0]:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = success[1]  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # Update 'home_page_url' to your actual home page URL name

