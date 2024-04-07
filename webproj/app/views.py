from django.shortcuts import render

from app import triplestore

# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def wizard_detail(request, wizard_id):
    
    wizard_data = triplestore.get_wizard_info(wizard_id)
    
    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

def test(request):
    
    triplestore.create_new_wizard(None, None, None, None, None, None, None, None, None, None)
    
    return 