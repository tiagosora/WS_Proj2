from app.triplestore.get_models import get_student_info
from app.triplestore.utils import execute_sparql_query

def get_house_info():
    """
        returns the sum of all student per course, taking only into consideration the courses being currently learned.
    """
    query_name = "app/queries/get_house_points.sparql"
    results, _ = execute_sparql_query(query_name=query_name, format='JSON')

    houses_info = {}
    for elem in results["results"]["bindings"]:
        houses_info[elem["name"]["value"]] = elem["totalPoints"]["value"]
        
    return houses_info

