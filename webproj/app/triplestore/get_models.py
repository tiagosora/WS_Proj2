from rdflib import Literal, URIRef
from app.models import Course, Professor, Student, Wizard
from app.triplestore.utils import execute_sparql_query
from app.triplestore.skills import get_skill_info


def get_professor(professor_uri):
    query_name = "app/queries/get_entity_info_by_uri.sparql"

    _, g = execute_sparql_query(query_name, format="turtle", uri=professor_uri)

    professor_attrs = {'learned': [], 'is_learning': []}
    for _, p, o in g:
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        professor_attrs[prop] = value

    professor = Professor(**professor_attrs)
    return professor

def get_wizard_info_by_uri(wizard_uri):
    query_name = "app/queries/get_entity_info_by_uri.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", uri=wizard_uri)

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

def get_student_info(student_uri):
    query_name = "app/queries/get_entity_info_by_uri.sparql"

    _, g = execute_sparql_query(query_name, format="turtle", uri=student_uri)

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

def get_course_info(course_uri):
    query_name = "app/queries/get_entity_info_by_uri.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", uri=course_uri)

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