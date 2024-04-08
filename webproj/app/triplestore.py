import json

from SPARQLWrapper import SPARQLWrapper, JSON, POST
from django.conf import settings
from rdflib import Graph, URIRef, Literal

from app.models import Wizard, Skill, Student, Course, Spell

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
sparql_update = SPARQLWrapper(settings.GRAPHDB_ENDPOINT_UPDATE)


def get_skill_info(skill_uri):
    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>
    DESCRIBE <{skill_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

    skill_attrs = {}
    for s, p, o in g.triples((URIRef(skill_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        skill_attrs[prop] = value

    return Skill(**skill_attrs)


def get_wizard_info(wizard_id):
    wizard_uri = f"http://hogwarts.edu/wizards/{wizard_id}"
    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>
    DESCRIBE <{wizard_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

    wizard_attrs = {'id': wizard_id, 'skills': [], 'spells': []}
    for s, p, o in g:
        prop = p.split('#')[-1]
        if prop == 'has_skill':
            skill_info = get_skill_info(str(o))
            wizard_attrs['skills'].append(skill_info)
        elif prop == 'has_spell':
            # Process spells similarly if you have a Spell class
            pass
        else:
            if isinstance(o, Literal):
                value = o.toPython()
            else:
                value = str(o)
            wizard_attrs[prop] = value

    wizard = Wizard(**wizard_attrs)
    return wizard


def get_wizard_info_by_uri(wizard_uri):
    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>
    DESCRIBE <{wizard_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

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

    max_wizard_id = max_student_id = max_account_id = house_id = None

    max_ids_query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT 
            (MAX(xsd:integer(?wizardId)) AS ?nextWizardId) 			
            (MAX(xsd:integer(?studentId)) AS ?nextStudentId)
            (MAX(xsd:integer(?accountId)) AS ?nextAccountId)
        WHERE {{
            ?wizard rdfs:type "wizard" .
            ?wizard hogwarts:id ?wizardId .
            ?student rdfs:type "student" .
            ?student hogwarts:id ?studentId .
            ?account rdfs:type "account" . 
            ?account hogwarts:id ?accountId .
        }}
    """

    sparql.setQuery(max_ids_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    max_wizard_id = int(results["results"]["bindings"][0]["nextWizardId"]["value"]) + 1
    max_student_id = int(results["results"]["bindings"][0]["nextStudentId"]["value"]) + 1
    max_account_id = int(results["results"]["bindings"][0]["nextAccountId"]["value"]) + 1

    house = house if bool(house) else ""

    house_id_query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT 
            ?houseId
        WHERE {{
            ?house rdfs:type "house" .
            ?house hogwarts:name ?houseName .
            FILTER(LCASE(?houseName) = LCASE("{house}")) . 
            ?house hogwarts:id ?houseId .
        }}
    """

    sparql.setQuery(house_id_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

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

    query_add = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {{
        GRAPH <http://hogwarts.edu/ontology#> {{
            
                <http://hogwarts.edu/wizards/{max_wizard_id}> 
                    hogwarts:id "{max_wizard_id}" ;
                    rdfs:type "wizard" ;
                    hogwarts:name "{name}" ;
                    {gender}
                    {species}
                    {blood_type}
                    {eye_color}
                    {house}
                    {wand}
                    {patronus} .

                <http://hogwarts.edu/accounts/{max_account_id}> 
                    hogwarts:id "{max_account_id}";
                    rdfs:type "account" ;
                    hogwarts:number "{nmec}" ;
                    hogwarts:password "{password}" ;
                    hogwarts:wizard <http://hogwarts.edu/wizards/{max_wizard_id}> .


                <http://hogwarts.edu/students/{max_student_id}> 
                    hogwarts:id "{max_student_id}" ;
                    rdfs:type "student" ;
                    hogwarts:school <http://hogwarts.edu/schools/1> ;
                    hogwarts:school_year "1" ;
                    hogwarts:wizard <http://hogwarts.edu/wizards/{max_wizard_id}> .
        }}
        }}
    """

    sparql_update.setMethod(POST)
    sparql_update.setQuery(query_add)
    sparql_update.query()

    return True, max_wizard_id


def check_if_nmec_exists(nmec):
    query_check = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>

        ASK WHERE {{
            ?student rdfs:type "account" .
            ?student hogwarts:number "{nmec}" .
        }}
    """

    sparql.setQuery(query_check)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return bool(results["boolean"])


def login(nmec, password):
    nmec_literal = f'"{nmec}"'
    password_literal = f'"{password}"'

    query_login = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT 
        ?wizardId
        WHERE 
        {{
            ?account rdfs:type "account" . 
            ?account hogwarts:number {nmec_literal} .
            ?account hogwarts:password {password_literal} .
            ?account hogwarts:wizard ?wizard .
            ?wizard hogwarts:id ?wizardId 
        }}
    """

    sparql.setQuery(query_login)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"]) > 0 and results["results"]["bindings"][0]["wizardId"]["value"]:
        wizard_id = int(results["results"]["bindings"][0]["wizardId"]["value"])
    else:
        return False, None

    return True, wizard_id


def get_role_info_by_wizard_id(wizard_id):
    """
        Returns the type of wizard from 3 possible: student, professor or headmaster. \n
        Returns None, None, None if it can't find any wizard in the database.
    """

    query_role = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?type ?role ?type_id
        WHERE {{
            ?wizard rdfs:type "wizard" . 
            ?wizard hogwarts:id "{wizard_id}" .
            OPTIONAL {{
                ?role hogwarts:wizard ?wizard .
                ?role rdfs:type ?type .
                ?role hogwarts:id ?type_id .
                FILTER (?type IN ("headmaster", "professor", "student"))
            }}
        }}
    """

    sparql.setQuery(query_role)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if (len(results["results"]["bindings"]) <= 0):
        return None, None, None

    wizard_type = results["results"]["bindings"][0]["type"]["value"]
    wizard_role = results["results"]["bindings"][0]["role"]["value"]
    wizard_type_id = results["results"]["bindings"][0]["type_id"]["value"]

    return wizard_type, wizard_role, wizard_type_id


def get_student_view_info(student_id):
    student_uri = f"http://hogwarts.edu/students/{student_id}"
    query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/>
        DESCRIBE <{student_uri}>
    """

    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

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


def get_course_info(course_uri):
    query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/>
        DESCRIBE <{course_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

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


def manage_spells_list(spells_uri):
    spells = []
    for spell in spells_uri:
        spells.append(get_spell_info(spell).info())

    return spells


def get_spell_info(spell_uri):
    query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/>
        DESCRIBE <{spell_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

    spell_attrs = {'teaches_spell': []}
    for s, p, o in g.triples((URIRef(spell_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        spell_attrs[prop] = value.replace("\xa0", " ") if bool(value) else "Unknown"

    spell = Spell(**spell_attrs)

    return spell


def get_professor_name(professor_uri):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        SELECT 
            ?name
        WHERE {{
            <{professor_uri}> hogwarts:wizard ?wizard .
            ?wizard hogwarts:name ?name
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


def get_house_name(houseId):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        SELECT 
            ?name
        WHERE {{
            <http://hogwarts.edu/houses/{houseId}> hogwarts:name ?name .
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


def get_school_name(school_uri):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        SELECT 
            ?name
        WHERE {{
            <{school_uri}> hogwarts:name ?name .
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name

def get_len_all_spells():
    query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT (COUNT(?spells) AS ?count)
        WHERE {{
            ?spells rdfs:type "spell" . 
        }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if len(results["results"]["bindings"]) > 0:
        return int(results["results"]["bindings"][0]["count"]["value"])
        
    return None