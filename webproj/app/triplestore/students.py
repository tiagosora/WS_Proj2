from app.triplestore.get_models import get_student_info
from app.triplestore.utils import execute_sparql_query


def get_number_students_is_learning_per_course_id():
    """
        returns the sum of all student per course, taking only into consideration the courses being currently learned.
    """
    query_name = "app/queries/get_students_per_course_is_learning.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON')
    
    len_courses = {}
    if (len(results["results"]["bindings"])>0):
        for elem in results["results"]["bindings"]:
            course_id = elem["id"]["value"]
            number_students = int(elem["numberOfStudents"]["value"])
            len_courses[course_id] = number_students

    return len_courses

def get_number_student_all_per_course_id():
    """
        returns the sum of all student per course, whether a student has learned or is currently learning. 
    """
    len_courses = get_number_students_is_learning_per_course_id()
    
    query_name = "app/queries/get_students_per_course_learned.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON')
    
    if (len(results["results"]["bindings"])>0):
        for elem in results["results"]["bindings"]:
            course_id = elem["id"]["value"]
            number_students = int(elem["numberOfStudents"]["value"])
            if course_id in len_courses: 
                len_courses[course_id] += number_students
            else:
                len_courses[course_id] = number_students

    return len_courses

def students_per_school_year():
    """
        returns the number of students for each year 
    """
    
    query_name = "app/queries/get_students_per_school_year.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON')

    students_per_year = {}
    if (len(results["results"]["bindings"])>0):
        for elem in results["results"]["bindings"]:
            school_year = elem["school_year"]["value"]
            number_students = int(elem["numberOfStudents"]["value"])
            students_per_year[school_year] = number_students

    return students_per_year

def get_students_enrolled(course_id):
    from app.triplestore.wizards import get_wizard_info_by_uri
    
    query_name = "app/queries/get_students_enrolled_course.sparql"
    results, _ = execute_sparql_query(query_name, format="JSON", course_id=course_id)
    
    
    students_enrolled = []
    for elem in results["results"]["bindings"]:
        student_uri = elem["student"]["value"]
        student = get_student_info(student_uri)
        wizard = get_wizard_info_by_uri(student.wizard)
        
        student_information = {}

        student_information.update({"student_id": student.id})
        student_information.update({"attending_year": student.school_year})
        student_information.update(wizard.info())
        student_information.update({"skills": [skill.name for skill in wizard.skills]})

        students_enrolled.append(student_information)

    return students_enrolled

def get_students_finished_course(course_id):
    from app.triplestore.wizards import get_wizard_info_by_uri
    
    query_name = "app/queries/get_students_made_course.sparql"
    results, _ = execute_sparql_query(query_name, format="JSON", course_id=course_id)
    
    
    students_finished = []
    for elem in results["results"]["bindings"]:
        student_uri = elem["student"]["value"]
        student = get_student_info(student_uri)
        wizard = get_wizard_info_by_uri(student.wizard)
        
        student_information = {}

        student_information.update({"student_id": student.id})
        student_information.update({"attending_year": student.school_year})
        student_information.update(wizard.info())
        student_information.update({"skills": [skill.name for skill in wizard.skills]})

        students_finished.append(student_information)

    return students_finished

