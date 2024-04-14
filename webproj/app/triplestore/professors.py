from app.triplestore.courses import get_courses_uri_by_professor_uri
from app.triplestore.get_models import get_course_info, get_professor
from app.triplestore.names_and_ids import get_school_name
from app.triplestore.spells import manage_spells_list
from app.triplestore.students import get_students_enrolled


def get_professor_info(professor_id):
    from app.triplestore.wizards import get_wizard_info_by_uri
    
    professor_uri = f"http://hogwarts.edu/professors/{professor_id}"
    
    professor = get_professor(professor_uri)
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