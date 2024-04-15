from app.decorators import (headmaster_required, logout_required,
                            professor_required, student_required)
from app.triplestore.courses import (get_courses_dict,
                                     update_is_learning_to_learned)
from app.triplestore.professors import get_professor_info
from app.triplestore.spells import get_len_all_spells
from app.triplestore.students import students_per_school_year
from app.triplestore.wizards import (create_new_wizard, get_all_students_info,
                                     get_headmaster_info,
                                     get_role_info_by_wizard_id,
                                     get_student_view_info, wizard_login)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


def authentication(request):
    return render(request, 'app/login.html')

# Create your views here.

@login_required
def index(request):
    return render(request, 'app/index.html')


@student_required
def student_dashboard(request):
    student_info = request.session['student_info']

    student = student_info['student']
    is_learning_courses = student_info['is_learning_courses']
    learned_courses = student_info['learned_courses']

    total_number_of_spells = get_len_all_spells()

    spells_per_course = {}
    for course in learned_courses:
        spells_per_course[course["name"]] = len(course["spells"])

    spells_acquired = []
    for course in learned_courses:
        for spell in course["spells"]:
            spells_acquired.append(spell)

    number_of_spells_not_acquired = total_number_of_spells - len(spells_acquired)

    paginator = Paginator(spells_acquired, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    skills = [skill["name"] for skill in student_info["skills"]]
    

    return render(request, 'app/student_dashboard.html', {
        'student': student,
        'is_learning_courses': is_learning_courses,
        'learned_courses': learned_courses,
        'spells_acquired': spells_acquired,
        'skills': ", ".join(skills),
        'number_of_spells_not_acquired': number_of_spells_not_acquired,
        'spells_per_course': spells_per_course,
        'page_obj': page_obj,
    })


@professor_required
def professor_dashboard(request):
    professor_info = request.session['professor_info']
    return render(request, 'app/professor_dashboard.html', {
        'professor': professor_info["professor"],
        'courses': professor_info["courses"],
    })


@headmaster_required
def headmaster_dashboard(request):
    headmaster_info = request.session['headmaster_info']
    students_list = get_all_students_info()
    students_list.sort(key = lambda student : (student["name"], student["gender"], student["blood_type"]))
    
    courses =  get_courses_dict()
    courses_in_list = []
    for id, course in courses.items():
        course["id"] = id
        course["number_spells_taught"] = len(course["spells"])
        courses_in_list.append(course)
    
    courses_in_list.sort(key = lambda course : (course["attending_year"], course["name"]))
    
    return render(request, 'app/headmaster_dashboard.html', {
        'headmaster': headmaster_info,
        'students_per_school_year': students_per_school_year(),
        'students' : students_list,
        'courses': courses_in_list,
    })

@headmaster_required
def course_view(request):
    course_id = request.POST.get('course_id')
    request.session['back'] = 'back'
    
    course_full_info = { 'name': 'Potions', 'attending_year': '1', 'type': 'Core', 'spells': [ { 'id': '6', 'effect': 'Grows antlers on head', 'incantation': 'Anteoculatia', 'light': 'Red', 'name': 'Hex that grows antlers on the head', 'type': 'Hex' }, { 'id': '19', 'effect': 'Small explosion', 'incantation': 'Bombarda', 'light': '', 'name': 'Exploding Charm', 'type': 'Charm' }, { 'id': '32', 'effect': 'Explosion', 'incantation': 'Confringo', 'light': 'Fiery Orange', 'name': 'Blasting Curse', 'type': 'Curse' }, { 'id': '45', 'effect': 'Turns object into dragon', 'incantation': 'Draconifors', 'light': 'Fiery orange', 'name': 'Draconifors Spell', 'type': 'Transfiguration' }, { 'id': '58', 'effect': 'Disarms an opponent', 'incantation': 'Expelliarmus', 'light': 'Scarlet', 'name': 'Disarming Charm', 'type': 'Charm' }, { 'id': '70', 'effect': 'Multiple concealing smokescreens', 'incantation': 'Fumos Duo', 'light': 'Dark Red', 'name': 'Fumos Duo', 'type': 'Charm' }, { 'id': '81', 'effect': 'Makes text illegible', 'incantation': 'Illegibilus', 'light': '', 'name': 'Illegibilus', 'type': 'Charm' }, { 'id': '93', 'effect': 'Sticks tongue to roof of the mouth', 'incantation': 'Langlock', 'light': '', 'name': 'Langlock', 'type': 'Jinx' }, { 'id': '104', 'effect': "Temporarily increases casters' spell power", 'incantation': 'Magicus Extremos', 'light': 'Pink', 'name': 'Magicus Extremos', 'type': 'Charm' }, { 'id': '116', 'effect': 'Extinguishes wandlight', 'incantation': 'Nox', 'light': '', 'name': 'Wand-Extinguishing Charm', 'type': 'Charm' }, { 'id': '127', 'effect': 'Parts the target', 'incantation': 'Partis Temporus', 'light': '', 'name': 'Partis Temporus', 'type': 'Charm' }, { 'id': '139', 'effect': 'Summons a large protective barrier', 'incantation': 'Protego Maxima', 'light': 'White', 'name': 'Protego Maxima', 'type': 'Charm' }, { 'id': '153', 'effect': 'Reveals secrets about a person or object', 'incantation': 'Revelio', 'light': 'Blue', 'name': 'Revelio Charm', 'type': 'Charm' }, { 'id': '165', 'effect': 'Softens objects', 'incantation': 'Spongify', 'light': 'Purple or Orange', 'name': 'Softening Charm', 'type': 'Charm' }, { 'id': '176', 'effect': 'Causes the wand tip to burn like a sparkler whilst damaging the foe', 'incantation': 'Verdillious', 'light': 'Green', 'name': 'Verdillious', 'type': 'Charm' } ], 'is_learning': [ { 'student_id': '5', 'attending_year': '1', 'id': '7', 'name': 'Fred Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '6', 'attending_year': '1', 'id': '8', 'name': 'George Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '11', 'attending_year': '1', 'id': '13', 'name': 'James Potter', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Hazel', 'wand': '', 'patronus': 'Stag', 'skills': [ ] }, { 'student_id': '15', 'attending_year': '1', 'id': '18', 'name': 'William Arthur Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Blue', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '18', 'attending_year': '1', 'id': '21', 'name': 'Oliver Wood', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '19', 'attending_year': '1', 'id': '22', 'name': 'Angelina Johnson', 'gender': 'Female', 'species': 'Human', 'blood_type': '', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '29', 'attending_year': '1', 'id': '33', 'name': 'Quirinus Quirrell', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '9" Alder unicorn hair bendy', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '35', 'attending_year': '1', 'id': '41', 'name': 'Padma Patil', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Prefect' ] }, { 'student_id': '36', 'attending_year': '1', 'id': '42', 'name': 'Michael Corner', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': 'Squirrel', 'skills': [ 'Potions' ] }, { 'student_id': '37', 'attending_year': '1', 'id': '43', 'name': 'Marietta Edgecombe', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Grey', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '38', 'attending_year': '1', 'id': '44', 'name': 'Terry Boot', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ 'Potions' ] }, { 'student_id': '42', 'attending_year': '1', 'id': '49', 'name': 'Gregory Goyle', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '45', 'attending_year': '1', 'id': '54', 'name': 'Narcissa Malfoy', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Blue', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '52', 'attending_year': '1', 'id': '61', 'name': 'Millicent Bulstrode', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '63', 'attending_year': '1', 'id': '79', 'name': 'Fat Friar', 'gender': 'Male', 'species': 'Ghost', 'blood_type': '', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ 'Curing peasants of the pox' ] }, { 'student_id': '71', 'attending_year': '1', 'id': '89', 'name': 'Dennis Creevey', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '76', 'attending_year': '1', 'id': '94', 'name': 'Rose Granger-Weasley', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] } ], 'learned': [ { 'student_id': '1', 'attending_year': '2', 'id': '1', 'name': 'Harry James Potter', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Bright green', 'wand': '11" Holly phoenix feather', 'patronus': 'Stag', 'skills': [ 'Duelling', 'Defence against the dark arts', 'Parseltongue', 'Seeker' ] }, { 'student_id': '2', 'attending_year': '2', 'id': '2', 'name': 'Ronald Bilius Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Blue', 'wand': '12" Ash unicorn tail hair', 'patronus': 'Jack Russell terrier', 'skills': [ 'Wizard chess' ] }, { 'student_id': '3', 'attending_year': '4', 'id': '3', 'name': 'Hermione Jean Granger', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': 'Brown', 'wand': '10¾" vine wood dragon heartstring', 'patronus': 'Otter', 'skills': [ 'Almost everything' ] }, { 'student_id': '4', 'attending_year': '5', 'id': '6', 'name': 'Neville Longbottom', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '13" Cherry unicorn hair', 'patronus': 'Non-corporeal', 'skills': [ 'Herbology' ] }, { 'student_id': '7', 'attending_year': '2', 'id': '9', 'name': 'Ginevra Molly Weasley', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Bright brown', 'wand': '', 'patronus': 'Horse', 'skills': [ 'Bat-Bogey hex' ] }, { 'student_id': '8', 'attending_year': '4', 'id': '10', 'name': 'Dean Thomas', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '9', 'attending_year': '3', 'id': '11', 'name': 'Seamus Finnigan', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '', 'patronus': 'Fox', 'skills': [ 'Pyrotechnics' ] }, { 'student_id': '10', 'attending_year': '2', 'id': '12', 'name': 'Lily J. Potter', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': 'Bright green', 'wand': '', 'patronus': 'Doe', 'skills': [ ] }, { 'student_id': '12', 'attending_year': '4', 'id': '14', 'name': 'Sirius Black', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '13', 'attending_year': '5', 'id': '16', 'name': 'Peter Pettigrew', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Blue', 'wand': '9¼" Chestnut dragon heartstring', 'patronus': '', 'skills': [ ] }, { 'student_id': '14', 'attending_year': '5', 'id': '17', 'name': 'Percy Ignatius Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Blue', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '16', 'attending_year': '3', 'id': '19', 'name': 'Charles Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': '12" Ash unicorn tail hair', 'patronus': '', 'skills': [ ] }, { 'student_id': '17', 'attending_year': '2', 'id': '20', 'name': 'Lee Jordan', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '20', 'attending_year': '5', 'id': '23', 'name': 'Katie Bell', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '21', 'attending_year': '2', 'id': '24', 'name': 'Alicia Spinnet', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '22', 'attending_year': '2', 'id': '25', 'name': 'Lavender Brown', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Blue', 'wand': '', 'patronus': '', 'skills': [ 'Divination' ] }, { 'student_id': '23', 'attending_year': '5', 'id': '26', 'name': 'Parvati Patil', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': '', 'skills': [ 'Divination' ] }, { 'student_id': '24', 'attending_year': '5', 'id': '27', 'name': 'Romilda Vane', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '25', 'attending_year': '5', 'id': '28', 'name': 'Colin Creevey', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ 'Photography' ] }, { 'student_id': '26', 'attending_year': '3', 'id': '29', 'name': 'Cormac McLaggen', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '27', 'attending_year': '2', 'id': '31', 'name': 'Molly Weasley', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Bright brown', 'wand': '', 'patronus': '', 'skills': [ 'Herbology', 'Household spells', 'Potions' ] }, { 'student_id': '28', 'attending_year': '2', 'id': '32', 'name': 'Arthur Weasley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Green', 'wand': '', 'patronus': 'Weasel', 'skills': [ 'Muggle world works' ] }, { 'student_id': '30', 'attending_year': '3', 'id': '34', 'name': 'Cho Chang', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': 'Swan', 'skills': [ 'Seeker' ] }, { 'student_id': '31', 'attending_year': '3', 'id': '35', 'name': 'Luna Lovegood', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Pale silvery', 'wand': '', 'patronus': 'Hare', 'skills': [ 'Spotting Nargles' ] }, { 'student_id': '32', 'attending_year': '3', 'id': '36', 'name': 'Gilderoy Lockhart', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Blue', 'wand': '9" Cherry dragon heartstring', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '33', 'attending_year': '3', 'id': '39', 'name': 'Garrick Ollivander', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Silvery', 'wand': '12¾" Hornbeam dragon heartstring', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '34', 'attending_year': '3', 'id': '40', 'name': 'Myrtle Elizabeth Warren (Moaning Myrtle)', 'gender': 'Female', 'species': 'Ghost', 'blood_type': 'Muggle-born', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '39', 'attending_year': '3', 'id': '45', 'name': 'Anthony Goldstein', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Grey', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Prefect' ] }, { 'student_id': '40', 'attending_year': '3', 'id': '47', 'name': 'Draco Malfoy', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': '10" Hawthorn unicorn hair', 'patronus': '', 'skills': [ 'Prefect' ] }, { 'student_id': '41', 'attending_year': '2', 'id': '48', 'name': 'Vincent Crabbe', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Black', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '43', 'attending_year': '5', 'id': '50', 'name': 'Bellatrix Lestrange', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '12¾" Walnut dragon heartstring', 'patronus': '', 'skills': [ ] }, { 'student_id': '44', 'attending_year': '2', 'id': '53', 'name': 'Lucius Malfoy', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': 'Elm and dragon heartstring', 'patronus': '', 'skills': [ ] }, { 'student_id': '46', 'attending_year': '3', 'id': '55', 'name': 'Regulus Arcturus Black', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Seeker' ] }, { 'student_id': '47', 'attending_year': '5', 'id': '56', 'name': 'Pansy Parkinson', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ 'Prefect' ] }, { 'student_id': '48', 'attending_year': '4', 'id': '57', 'name': 'Blaise Zabini', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '49', 'attending_year': '4', 'id': '58', 'name': 'Tom Marvolo Riddle', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Scarlet', 'wand': '13½" Yew phoenix feather core', 'patronus': '', 'skills': [ ] }, { 'student_id': '50', 'attending_year': '2', 'id': '59', 'name': 'Theodore Nott', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '51', 'attending_year': '2', 'id': '60', 'name': 'Rodolphus Lestrange', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '53', 'attending_year': '5', 'id': '62', 'name': 'Graham Montague', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '54', 'attending_year': '3', 'id': '63', 'name': 'Bloody Baron', 'gender': 'Male', 'species': 'Ghost', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '55', 'attending_year': '4', 'id': '64', 'name': 'Marcus Flint', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '56', 'attending_year': '3', 'id': '65', 'name': 'Penelope Clearwater', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Muggle-born or half-blood', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Prefect' ] }, { 'student_id': '57', 'attending_year': '5', 'id': '66', 'name': 'Roger Davies', 'gender': 'Male', 'species': 'Human', 'blood_type': '', 'eye_color': 'Dark', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '58', 'attending_year': '5', 'id': '67', 'name': 'Marcus Belby', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Dark', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '59', 'attending_year': '2', 'id': '71', 'name': 'Nicholas de Mimsy-Porpington', 'gender': 'Male', 'species': 'Ghost', 'blood_type': '', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '60', 'attending_year': '4', 'id': '73', 'name': 'Barty Crouch Jr.', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Pale, freckled', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '61', 'attending_year': '5', 'id': '76', 'name': 'Alecto Carrow', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '62', 'attending_year': '4', 'id': '77', 'name': 'Amycus Carrow', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '64', 'attending_year': '2', 'id': '80', 'name': 'Helena Ravenclaw', 'gender': 'Female', 'species': 'Ghost', 'blood_type': 'Pure-blood or half-blood', 'eye_color': 'Grey', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '65', 'attending_year': '4', 'id': '83', 'name': 'Cedric Diggory', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': '12¼", Ash, unicorn hair', 'patronus': '', 'skills': [ ] }, { 'student_id': '66', 'attending_year': '4', 'id': '84', 'name': 'Justin Finch-Fletchley', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Muggle-born', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '67', 'attending_year': '5', 'id': '85', 'name': 'Zacharias Smith', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '68', 'attending_year': '4', 'id': '86', 'name': 'Hannah Abbott', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Brown', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '69', 'attending_year': '4', 'id': '87', 'name': 'Ernest Macmillan', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': '', 'wand': '', 'patronus': 'Boar', 'skills': [ ] }, { 'student_id': '70', 'attending_year': '3', 'id': '88', 'name': 'Susan Bones', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '72', 'attending_year': '2', 'id': '90', 'name': 'Albus Severus Potter', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Bright green', 'wand': '', 'patronus': '', 'skills': [ 'Liaising with giants' ] }, { 'student_id': '73', 'attending_year': '5', 'id': '91', 'name': 'Scorpius Hyperion Malfoy', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Pure-blood', 'eye_color': 'Grey', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '74', 'attending_year': '3', 'id': '92', 'name': 'Edward Remus Lupin', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Variable', 'wand': '', 'patronus': '', 'skills': [ 'Duelling' ] }, { 'student_id': '75', 'attending_year': '4', 'id': '93', 'name': 'James Sirius Potter', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': '', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '77', 'attending_year': '5', 'id': '95', 'name': 'Argus Filch', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Squib', 'eye_color': 'Pale', 'wand': '', 'patronus': '', 'skills': [ ] }, { 'student_id': '78', 'attending_year': '4', 'id': '96', 'name': 'Poppy Pomfrey', 'gender': 'Female', 'species': 'Human', 'blood_type': 'Pure-blood or half-blood', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ ] }, { 'student_id': '79', 'attending_year': '3', 'id': '97', 'name': 'Rolanda Hooch', 'gender': 'Female', 'species': 'Human', 'blood_type': '', 'eye_color': 'Yellow', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Auror' ] }, { 'student_id': '80', 'attending_year': '3', 'id': '98', 'name': 'Irma Pince', 'gender': 'Female', 'species': 'Human', 'blood_type': '', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ 'Auror' ] }, { 'student_id': '81', 'attending_year': '4', 'id': '101', 'name': 'Wilhelmina Grubbly-Plank', 'gender': 'Female', 'species': 'Human', 'blood_type': '', 'eye_color': '', 'wand': '', 'patronus': 'Non-corporeal', 'skills': [ ] } ], 'professor_info': { 'id': '46', 'name': 'Severus Snape', 'gender': 'Male', 'species': 'Human', 'blood_type': 'Half-blood', 'eye_color': 'Black', 'wand': '', 'patronus': 'Doe' } }
    
    # get_course_by_id_dict(course_id)
    course_full_info['number_students_enrolled'] = len(course_full_info['is_learning'])


        
    return render(request, 'app/course.html', {
        'course': course_full_info,
    })
    
@headmaster_required
def remove_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')
    
    return redirect("course_dashboard")

@logout_required
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

        success, id_number = create_new_wizard(password, blood_type, eye_color, gender, house, nmec, name, patronus,
                                    species, wand)  # Fill in other parameters
        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in

            wizard_info, _, wizard_type_id = get_role_info_by_wizard_id(id_number)

            match wizard_info:
                case 'student':
                    request.session['student_info'] = get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                # case 'profesor':
                #     return professor_dashboard(request)  # TODO: mudar para pagina do professor
                # case 'headmaster':
                #     return professor_dashboard(request)  # TODO: mudar para pagina do professor
                case _:
                    logout(request)
                    return redirect("index")

        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})

    return render(request, 'registration/login.html')

@login_required
def back_to_dashboard(request):
    wizard_info = request.session['role']
    del request.session['back']
    match wizard_info:
        case 'student':
            return redirect("student_dashboard")
        case 'professor':
            return redirect("professor_dashboard")
        case 'headmaster':
            return redirect("headmaster_dashboard")
        case _:
            logout(request)
            return redirect("index")

@logout_required
def login_view(request):
    if request.method == 'POST':
        nmec = request.POST.get('id_number')
        password = request.POST.get('password')

        success, id_number = wizard_login(nmec, password)

        if success:
            request.session['nmec'] = nmec
            request.session['wizard_id'] = id_number  # An example of user identification
            request.session['authenticated'] = True  # Indicate the user is logged in

            # ver qual o role da pessoa que se autenticou e ir para a pagina correspondente
            wizard_info, _, wizard_type_id = get_role_info_by_wizard_id(id_number)

            request.session['role'] = wizard_info
            request.session['wizard_type_id'] = wizard_type_id
            
            print(wizard_info)
            
            match wizard_info:
                case 'student':
                    request.session['student_info'] = get_student_view_info(wizard_type_id)
                    return redirect("student_dashboard")
                case 'professor':
                    request.session['professor_info'] = get_professor_info(wizard_type_id)
                    return redirect("professor_dashboard")
                case 'headmaster':
                    request.session['headmaster_info'] = get_headmaster_info(wizard_type_id)
                    return redirect("headmaster_dashboard")
                case _:
                    logout(request)
                    return redirect("index")
        else:
            return render(request, 'registration/login.html', {'error': 'Registration failed.'})
    return render(request, 'registration/login.html')

@require_http_methods(["POST"])
def pass_student(request):
    student_id = request.POST.get('student_id')
    course_id = request.POST.get('course_id')

    update_is_learning_to_learned(course_id, student_id)
    
    request.session['professor_info'] = get_professor_info(request.session['wizard_type_id'])
    return redirect("professor_dashboard")

@login_required(redirect_field_name="")
def logout_view(request):
    logout(request)
    return redirect('index')
