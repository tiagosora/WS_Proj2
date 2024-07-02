from app.triplestore.courses import (add_spell_to_course,
                                     add_student_to_course,
                                     change_course_professor,
                                     get_course_by_id_dict,
                                     remove_spell_from_course,
                                     remove_student_from_course,
                                     update_is_learning_to_learned)
from app.triplestore.professors import (get_all_teachers_not_teaching_course,
                                        get_professor_info)
from app.triplestore.students import (get_spells_not_taught_in_course,
                                      get_students_not_learning_course)
from app.triplestore.wizards import get_all_students_info
from django.shortcuts import redirect, render


def course_view(request):
    course_id = request.POST.get('course_id')
    if not course_id:
        course_id = request.session['course_id']
    request.session['course_id'] = course_id
    request.session['back'] = 'back'
    
    students_list = get_all_students_info()
    students_list.sort(key=lambda student: (student["name"], student["gender"], student["blood_type"]))

    course_full_info = get_course_by_id_dict(course_id)

    course_full_info['number_students_enrolled'] = len(course_full_info['is_learning'])
    course_full_info['number_spells_taught'] = len(course_full_info['spells'])

    available_professors = get_all_teachers_not_teaching_course(course_full_info['professor_info']['id'])
    available_professors.sort(key=lambda professor: professor['name'])

    return render(request, 'app/course.html', {
        'course': course_full_info,
        'students': students_list,
        'available_students': get_students_not_learning_course(course_id),
        'available_spells': get_spells_not_taught_in_course(course_id),
        'available_professors': available_professors,
    })

def remove_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    remove_student_from_course(course_id, student_id, not request.session.get('infering', True))

    return redirect("course")


def add_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    add_student_to_course(course_id, student_id, not request.session.get('infering', True))

    return redirect("course")


def remove_spell(request):
    spell_id = request.POST.get('spell_id')
    course_id = request.POST.get('course_id')

    remove_spell_from_course(course_id, spell_id, not request.session.get('infering', True))

    return redirect("course")


def add_spell(request):
    spell_id = request.POST.get('spell_id')
    course_id = request.POST.get('course_id')


    add_spell_to_course(course_id, spell_id, not request.session.get('infering', True))

    return redirect("course")


def change_professor(request):
    professor_id = request.POST.get('professor_id')
    course_id = request.POST.get('course_id')

    change_course_professor(course_id, professor_id, not request.session.get('infering', True))

    return redirect("course")


def pass_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    update_is_learning_to_learned(course_id, student_id, not request.session.get('infering', True))

    request.session['professor_info'] = get_professor_info(request.session['wizard_type_id'])
    return redirect("professor_dashboard")


