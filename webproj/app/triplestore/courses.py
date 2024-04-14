from rdflib import URIRef, Literal
from app.triplestore.utils import execute_sparql_query

from app.models import Course
from app.triplestore.spells import manage_spells_list
from app.triplestore.wizards import get_students_enrolled
from app.triplestore.get_models import get_professor, get_course_info, get_wizard_info_by_uri
from app.triplestore.students import get_students_finished_course


def get_courses_uri_by_professor_uri(professor_uri):
    query_name = "app/queries/get_courses_uri_by_professor_uri.sparql"
    
    results, _ = execute_sparql_query(query_name, format='JSON', user_uri=professor_uri)
    
    total_courses = []
    for elem in results["results"]["bindings"]:
        total_courses.append(elem["courses"]["value"])
        
    return total_courses

def update_learned_to_is_learning(course_id, student_id):   #teoricamente, useless
    query_name = "app/queries/update_learned_to_is_learning.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, student_id=student_id)
    
def get_courses_dict():
    
    query_name = "app/queries/get_all_by_type.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON', type="course")
    
    courses = []
    for elem in results["results"]["bindings"]:
        courses.append(get_course_info(elem["course"]["value"]))
        
    courses_dict = {course.id: course.info_no_id()
                | {'spells': manage_spells_list(course.teaches_spell)}
                | {'is_learning': get_students_enrolled(course.id)}
                | {'learned': get_students_finished_course(course.id)}
                | {'professor_info': get_wizard_info_by_uri(get_professor(course.professor).wizard).info()}
                for course in courses}
    
    return courses_dict

    
def update_is_learning_to_learned(course_id, student_id):
    query_name = "app/queries/update_is_learning_to_learned.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, student_id=student_id)
    
def add_spell_to_course(course_id, spell_id):
    query_name = "app/queries/add_spell_to_course.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, spell_id=spell_id)
    
def remove_spell_from_course(course_id, spell_id):
    query_name = "app/queries/remove_spell_from_course.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, spell_id=spell_id)
    
def add_student_to_course(course_id, student_id):
    query_name = "app/queries/add_student_to_course.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, student_id=student_id)

def remove_student_from_course(course_id, student_id):  #teoricamente, useless
    query_name = "app/queries/remove_student_from_course.sparql"
    execute_sparql_query(query_name=query_name, format='POST', course_id=course_id, student_id=student_id)
    
def get_len_all_courses():
    query_name = "app/queries/get_len_all_courses.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON')
    
    len_courses = None
    if (len(results["results"]["bindings"])>0):
        len_courses = int(results["results"]["bindings"][0]["count"]["value"])
        
    return len_courses