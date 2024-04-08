from SPARQLWrapper import SPARQLWrapper, JSON, POST
from app.models import Wizard, Skill, Student, Course, Spell
from django.conf import settings
from rdflib import Graph, URIRef, Literal

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
sparql_update = SPARQLWrapper(settings.GRAPHDB_ENDPOINT_UPDATE)


# DONE
def load_sparql_query(filename, **kwargs):
    with open(filename, 'r') as file:
        query_template = file.read()

    query = query_template.format(**kwargs)
    return query


def execute_sparql_query(query_name, format="turtle", **kwargs):
    g = Graph()
    results = None

    if format == "POST":
        query = load_sparql_query(query_name, **kwargs)
        sparql_update.setMethod(POST)
        sparql_update.setQuery(query)
        sparql_update.query()

    else:
        query = load_sparql_query(query_name, **kwargs)
        sparql.setQuery(query)
        if format == 'JSON':
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            g.parse(data=results, format='JSON')
        elif format == 'turtle':
            sparql.setReturnFormat('turtle')
            results = sparql.query().convert()
            g.parse(data=results, format='turtle')

    return results, g


# DONE
def get_skill_info(skill_uri):
    query_name = "app/queries/get_skill_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", skill_uri=skill_uri)

    skill_attrs = {}
    for s, p, o in g.triples((URIRef(skill_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        skill_attrs[prop] = value

    return Skill(**skill_attrs)


# DONE
def get_wizard_info_by_uri(wizard_uri):
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", wizard_uri=wizard_uri)

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


# DONE
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
    _, _ = execute_sparql_query(query_name, name=name, gender=gender,
                                species=species, blood_type=blood_type, eye_color=eye_color,
                                wand=wand, patronus=patronus, max_wizard_id=max_wizard_id,
                                house=house, max_account_id=max_account_id, nmec=nmec,
                                password=password, max_student_id=max_student_id)

    return True, max_wizard_id


# DONE
def check_if_nmec_exists(nmec):
    query_name = "app/queries/check_if_nmec_exists.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", nmec=nmec)

    return bool(results["boolean"])


# DONE
def login(nmec, password):
    nmec_literal = f'"{nmec}"'
    password_literal = f'"{password}"'

    query_name = "app/queries/login.sparql"

    results, _ = execute_sparql_query(query_name, nmec_literal=nmec_literal, password_literal=password_literal)

    if len(results["results"]["bindings"]) > 0 and results["results"]["bindings"][0]["wizardId"]["value"]:
        wizard_id = int(results["results"]["bindings"][0]["wizardId"]["value"])
    else:
        return False, None

    return True, wizard_id


# DONE
def get_role_info_by_wizard_id(wizard_id):
    query_name = "app/queries/get_role_info_by_wizard_id.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", wizard_id=wizard_id)

    if len(results["results"]["bindings"]) <= 0:
        return None, None, None

    wizard_type = results["results"]["bindings"][0]["type"]["value"]
    wizard_role = results["results"]["bindings"][0]["role"]["value"]
    wizard_type_id = results["results"]["bindings"][0]["type_id"]["value"]

    return wizard_type, wizard_role, wizard_type_id


# DONE
def get_student_view_info(student_id):
    student_uri = f"http://hogwarts.edu/students/{student_id}"
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", user_uri=student_uri)

    student_attrs = {'id': student_id, 'learned': [], 'is_learning': []}
    for s, p, o in g:
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

    student = Student(**student_attrs)
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

    skills = [skill.name for skill in wizard.skills]

    spells_aquired = []
    [spells_aquired.extend(spell['spells']) for spell in is_learning_courses]

    return {'student':
                wizard.info()
                | {'house_name': get_house_name(wizard.house)}
                | {'school_year': student.school_year}
                | {'school_name': get_school_name(student.school)},
            'is_learning_courses': is_learning_courses,
            'learned_courses': learned_courses,
            'spells_aquired': spells_aquired,
            'skills': skills
            }


# DONE
def get_course_info(course_uri):
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", user_uri=course_uri)

    course_attrs = {'teaches_spell': []}
    for s, p, o in g.triples((URIRef(course_uri), None, None)):
        prop = p.split('#')[-1]
        if prop == 'teaches_spell':
            course_attrs['teaches_spell'].append(str(o))
        else:
            if isinstance(o, Literal):
                value = o.toPython()
            else:
                value = str(o)
            course_attrs[prop] = value

    course = Course(**course_attrs)

    return course


# DONE
def manage_spells_list(spells_uri):
    spells = []
    for spell in spells_uri:
        spells.append(get_spell_info(spell).info())

    return spells

# DONE
def get_spell_info(spell_uri):
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", user_uri=spell_uri)

    spell_attrs = {'teaches_spell': []}
    for s, p, o in g.triples((URIRef(spell_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        spell_attrs[prop] = value.replace("\xa0", " ")

    spell = Spell(**spell_attrs)

    return spell


# DONE
def get_professor_name(professor_uri):
    query_name = "app/queries/get_professor_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", professor_uri=professor_uri)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


# DONE
def get_house_name(houseId):
    query_name = "app/queries/get_house_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", houseId=houseId)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


# DONE
def get_school_name(school_uri):
    query_name = "app/queries/get_school_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", school_uri=school_uri)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name