from app.triplestore.houses import get_house_info
from app.triplestore.students import remove_points
from app.triplestore.wizards import get_all_students_info
from django.shortcuts import redirect, render


def points_banners(request):
    request.session['back'] = 'back'
    
    students = get_all_students_info()
    students.sort(key=lambda student: (student["points"], student["star"], student["name"], student["gender"]), reverse=True)
    houses = get_house_info()
    
    print(students)
    
    return render(request, 'app/points_banners.html', {
        'students': students,
        'houses': houses
    })

def give_points(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        points = request.POST.get('points')
        
        remove_points(student_id, points, not request.session.get('infering', True))
    
    return redirect("points_banners")
