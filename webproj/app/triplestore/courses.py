from rdflib import URIRef, Literal
from app.triplestore.utils import execute_sparql_query

from app.models import Course


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

def get_courses_uri_by_professor_uri(professor_uri):
    query_name = "app/queries/get_courses_uri_by_professor_uri.sparql"
    
    results, _ = execute_sparql_query(query_name, format='JSON', user_uri=professor_uri)
    
    total_courses = []
    for elem in results["results"]["bindings"]:
        total_courses.append(elem["courses"]["value"])
        
    return total_courses

