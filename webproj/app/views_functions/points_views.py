from app.triplestore.houses import get_house_info
from app.triplestore.students import remove_points
from app.triplestore.wizards import (get_all_advanced_students_info,
                                     get_all_basic_students_info,
                                     get_all_medium_students_info,
                                     get_all_students_info)
from django.shortcuts import redirect, render


def points_banners(request):
    request.session['back'] = 'back'
    
    students = get_all_students_info()
    students.sort(key=lambda student: (student["points"], student["star"], student["name"], student["gender"]), reverse=True)
    houses = get_house_info()
    
    basic_students = get_all_basic_students_info()
    medium_student = get_all_medium_students_info()
    advanced_student = get_all_advanced_students_info()
    merged = basic_students + medium_student + advanced_student
    
    
    for student in students:
        for student_type in merged:
            if student["id"] == student_type["id"]:
                student["student_type"] = student_type["student_type"]
    
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
