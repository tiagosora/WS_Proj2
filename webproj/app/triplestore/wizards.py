from rdflib import Literal
from app.triplestore.names_and_ids import get_house_name, get_school_name, get_professor_name

from app.triplestore.spells import manage_spells_list

from app.triplestore.courses import get_course_info, get_courses_uri_by_professor_uri

from app.models import Student, Wizard, Professor
from app.triplestore.utils import execute_sparql_query, check_if_nmec_exists

from app.triplestore.skills import get_skill_info


def get_wizard_info_by_uri(wizard_uri):
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", user_uri=wizard_uri)

    wizard_attrs = {'skills': [], 'spells': []}
    for s, p, o in g:
        prop = p.split('#')[-1]
        if prop == 'has_skill':
            skill_info = get_skill_info(str(o))
            wizard_attrs['skills'].append(skill_info)
        else:
            if isinstance(o, Literal):
                value = o.toPython()
            else:
                value = str(o)
            wizard_attrs[prop] = value

    wizard = Wizard(**wizard_attrs)
    return wizard


def create_new_wizard(password: str, blood_type: str, eye_color: str, gender: str,
                      house: int, nmec: int, name: str,
                      patronus: str, species: str, wand: str):
    wand = wand.replace("\\", "\\\\").replace("\"", "\\\"")

    if not bool(password) or not bool(name) or not bool(nmec):
        return False, None

    if check_if_nmec_exists(nmec):
        return False, None

    house_id = None

    query_name = "app/queries/max_ids_info.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON")

    max_wizard_id = int(results["results"]["bindings"][0]["nextWizardId"]["value"]) + 1
    max_student_id = int(results["results"]["bindings"][0]["nextStudentId"]["value"]) + 1
    max_account_id = int(results["results"]["bindings"][0]["nextAccountId"]["value"]) + 1
    
    house = house if bool(house) else ""

    query_name = "app/queries/house_id_info.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", house=house)

    if len(results["results"]["bindings"]) > 0 and "houseId" in results["results"]["bindings"][0].keys():
        house_id = results["results"]["bindings"][0]["houseId"]["value"]

    house = "hogwarts:house \"" + house_id + "\" ;" if bool(house_id) else ""

    name = name if bool(name) else ""
    gender = "hogwarts:gender \"" + gender + "\" ;" if bool(gender) else ""
    species = "hogwarts:species \"" + species + "\" ;" if bool(species) else ""
    blood_type = "hogwarts:blood-type \"" + blood_type + "\" ;" if bool(blood_type) else ""
    eye_color = "hogwarts:eye_color \"" + eye_color + "\" ;" if bool(eye_color) else ""
    wand = "hogwarts:wand \"" + wand + "\" ;" if bool(wand) else ""
    patronus = "hogwarts:patronus \"" + patronus + "\" ;" if bool(patronus) else ""

    query_name = "app/queries/add_wizard.sparql"
    _, _ = execute_sparql_query(query_name, format="POST", name=name, gender=gender,
                                species=species, blood_type=blood_type, eye_color=eye_color,
                                wand=wand, patronus=patronus, max_wizard_id=max_wizard_id,
                                house=house, max_account_id=max_account_id, nmec=nmec,
                                password=password, max_student_id=max_student_id)

    return True, max_wizard_id


def wizard_login(nmec, password):
    nmec_literal = f'"{nmec}"'
    password_literal = f'"{password}"'

    query_name = "app/queries/login.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", nmec_literal=nmec_literal,
                                      password_literal=password_literal)

    if len(results["results"]["bindings"]) > 0 and results["results"]["bindings"][0]["wizardId"]["value"]:
        wizard_id = int(results["results"]["bindings"][0]["wizardId"]["value"])
    else:
        return False, None

    return True, wizard_id


def get_role_info_by_wizard_id(wizard_id):
    query_name = "app/queries/get_role_info_by_wizard_id.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", wizard_id=wizard_id)

    if len(results["results"]["bindings"]) <= 0:
        return None, None, None

    wizard_type = results["results"]["bindings"][0]["type"]["value"]
    wizard_role = results["results"]["bindings"][0]["role"]["value"]
    wizard_type_id = results["results"]["bindings"][0]["type_id"]["value"]

    return wizard_type, wizard_role, wizard_type_id


def get_student_info(student_uri):
    query_name = "app/queries/get_user_info.sparql"

    _, g = execute_sparql_query(query_name, format="turtle", user_uri=student_uri)

    student_attrs = {'learned': [], 'is_learning': []}
    for _, p, o in g:
        prop = p.split('#')[-1]
        if prop == 'learned':
            student_attrs['learned'].append(str(o))
        elif prop == 'is_learning':
            student_attrs['is_learning'].append(str(o))
        else:
            if isinstance(o, Literal):
                value = o.toPython()
            else:
                value = str(o)
            student_attrs[prop] = value

    return Student(**student_attrs)


def get_student_view_info(student_id):
    
    student_uri = f"http://hogwarts.edu/students/{student_id}"
    
    student = get_student_info(student_uri)
    wizard = get_wizard_info_by_uri(student.wizard)

    courses_is_learning_list = []
    for course in student.is_learning:
        courses_is_learning_list.append(get_course_info(course))

    courses_learned_list = []
    spells_learned = []
    for course in student.learned:
        temp_course = get_course_info(course)
        spells_learned.extend(temp_course.teaches_spell)
        courses_learned_list.append(temp_course)

    is_learning_courses = [course.info()
                           | {'spells': manage_spells_list(course.teaches_spell)}
                           | {'professor_name': get_professor_name(course.professor)}
                           for course in courses_is_learning_list]

    learned_courses = [course.info()
                       | {'spells': manage_spells_list(course.teaches_spell)}
                       | {'professor_name': get_professor_name(course.professor)}
                       for course in courses_learned_list]

    skills = [skill.info() for skill in wizard.skills]
    
    

    spells_acquired = []
    [spells_acquired.extend(spell['spells']) for spell in learned_courses]

    return {'student':
                wizard.info()
                | {'house_name': get_house_name(wizard.house)}
                | {'school_year': student.school_year}
                | {'school_name': get_school_name(student.school)},
            'is_learning_courses': is_learning_courses,
            'learned_courses': learned_courses,
            'spells_acquired': spells_acquired,
            'skills': skills
            }
    
    
def get_students_enrolled(course_id):
    query_name = "app/queries/get_students_enrolled_course.sparql"
    results, _ = execute_sparql_query(query_name, format="JSON", course_id=course_id)
    
    
    students_enrolled = []
    for elem in results["results"]["bindings"]:
        student_uri = elem["student"]["value"]
        student = get_student_info(student_uri)
        wizard = get_wizard_info_by_uri(student.wizard)
        
        student_information = {}
        print(student.id)
        student_information.update({"student_id": student.id})
        student_information.update({"attending_year": student.school_year})
        student_information.update(wizard.info())
        student_information.update({"skills": [skill.name for skill in wizard.skills]})

        students_enrolled.append(student_information)

    return students_enrolled
    
def get_professor_info(professor_id):
    professor_uri = f"http://hogwarts.edu/professors/{professor_id}"
    query_name = "app/queries/get_user_info.sparql"

    _, g = execute_sparql_query(query_name, format="turtle", user_uri=professor_uri)

    professor_attrs = {'id': professor_id, 'learned': [], 'is_learning': []}
    for _, p, o in g:
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        professor_attrs[prop] = value

    professor = Professor(**professor_attrs)
    wizard = get_wizard_info_by_uri(professor.wizard)
    
    professor_courses = get_courses_uri_by_professor_uri(professor_uri)
    
    total_professor_courses = []
    for course_uri in professor_courses:
        total_professor_courses.append(get_course_info(course_uri))
        
    professor_courses = [course.info()
                        | {'spells': manage_spells_list(course.teaches_spell)}
                        | {'students_enrolled': get_students_enrolled(course.id)}
                        for course in total_professor_courses]
    
    professor_info = {}
    professor_info.update({"courses": professor_courses})
    professor_info.update({"professor": wizard.info() | {"school_name": get_school_name(professor.school)} })
                        
                        
    return professor_info
