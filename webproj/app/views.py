from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app import triplestore

# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def wizard_detail(request, wizard_id):
    
    wizard_data = triplestore.get_wizard_info(wizard_id)
    
    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

@login_required
def index(request):
    return render(request, 'app/index.html')

def authentication(request):
    return render(request, 'app/authentication.html')
