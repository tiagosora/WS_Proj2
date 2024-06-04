from app.triplestore.courses import get_course_info
from app.triplestore.get_models import get_wizard_info_by_uri
from app.triplestore.names_and_ids import (get_house_name, get_professor_name,
                                           get_school_name)
from app.triplestore.spells import manage_spells_list
from app.triplestore.students import get_student_info
from app.triplestore.utils import check_if_nmec_exists, execute_sparql_query
from rdflib import Literal


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

    if len(results["results"]["bindings"]) > 0 and results["results"]["bindings"][0]["wizard"]["value"]:
        wizard_id = results["results"]["bindings"][0]["wizard"]["value"]
    else:
        return False, None

    return True, wizard_id


def get_role_info_by_wizard_id(wizard_id):
    query_name = "app/queries/get_role_info_by_wizard_id.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", wizard_id=wizard_id)

    if len(results["results"]["bindings"]) <= 0:
        return None, None, None

    wizard_type_id = results["results"]["bindings"][0]["role"]["value"]
    wizard_role = results["results"]["bindings"][0]["type"]["value"]

    return wizard_role, wizard_type_id


def get_all_students_info():
    query_name = "app/queries/get_all_by_type.sparql"

    results, _ = execute_sparql_query(query_name=query_name, format='JSON', type="Student")
    
    if len(results["results"]["bindings"]) <= 0:
        return []
    
    students = []
    for elem in results["results"]["bindings"]:
        wizard, student = student_info(student_uri=elem["data"]["value"])
        
        student_information = wizard.info() \
                            | {'house_name': get_house_name(wizard.house)} \
                            | {'school_year': student.school_year} \
                            | {'points': student.points}
        
        students.append(student_information)
        
    return students
    

def student_info(student_uri):
    student = get_student_info(student_uri)
    wizard = get_wizard_info_by_uri(student.wizard)

    return wizard, student
    
    
def get_student_view_info(student_id):
    student_uri = student_id
    
    wizard, student = student_info(student_uri=student_uri)
    
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


def get_headmaster_info(headmaster_id):
    headmaster_uri = f"{headmaster_id}"
    query_name = "app/queries/get_entity_info_by_uri.sparql"
    
    _, g = execute_sparql_query(query_name, format="turtle", uri=headmaster_uri)
    
    headmaster_attr = {}
    for _, p, o in g:
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        headmaster_attr[prop] = value
    
    if not all(key in headmaster_attr for key in ["hasAccount", "hasStartDate", "hasHeadmaster"]):
        return {}
    
    headmaster_start_date = headmaster_attr["hasStartDate"]
    
    headmaster_info = get_wizard_info_by_uri(headmaster_attr["hasAccount"]).info() | {"start_date": headmaster_start_date} 
    
    return headmaster_info


def update_wizard_info(wizard_id, name = None, gender = None, blood_type = None, species = None, eye_color = None, patronus = None, wand = None):
    
    query_delete = ""
    query_insert = ""
    
    if bool(name): 
        query_delete += "\t ?wizard :hasName ?old_name .\n"
        query_insert += f"\t ?wizard :hasName '{name}' .\n"
        
    if bool(gender):
        query_delete += "\t ?wizard :hasGender ?old_gender .\n"
        query_insert += f"\t ?wizard :hasGender '{gender}' .\n"
        
    if bool(blood_type):
        query_delete += "\t ?wizard :hasBloodType ?old_blood_type .\n"
        query_insert += f"\t ?wizard :hasBloodType '{blood_type}' .\n"
        
    if bool(species):
        query_delete += "\t ?wizard :hasSpecies ?old_species .\n"
        query_insert += f"\t ?wizard :hasSpecies '{species}' .\n"
        
    if bool(eye_color):
        query_delete += "\t ?wizard :hasEyeColor ?old_eye_color .\n"
        query_insert += f"\t ?wizard :hasEyeColor '{eye_color}' .\n"
        
    if bool(patronus):
        query_delete += "\t ?wizard :hasPatronus ?old_patronus .\n"
        query_insert += f"\t ?wizard :hasPatronus '{patronus}' .\n"
        
    if bool(wand):
        query_delete += "\t ?wizard :hasWand ?old_wand .\n"
        query_insert += f"\t ?wizard :hasWand '{wand}' .\n"
        
    query_name = "app/queries/update_wizard_info.sparql"
    execute_sparql_query(query_name=query_name, format='POST', wizard_id=wizard_id, query_delete=query_delete, query_insert=query_insert)