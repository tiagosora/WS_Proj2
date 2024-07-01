from app.triplestore.utils import execute_sparql_query


def infer_queries():
    print("Infering queries...")

    queries = [
        "app/inferences/remove_all_stars.sparql",
        "app/inferences/AdvancedStudent.sparql",
        "app/inferences/MediumStudent.sparql",
        "app/inferences/BasicStudent.sparql",
        "app/inferences/deleteTotalHousePoints.sparql",
        "app/inferences/inferHousePoints.sparql",
        "app/inferences/one_star.sparql",
        "app/inferences/two_star.sparql",
        "app/inferences/three_star.sparql",
        "app/inferences/four_star.sparql",
        "app/inferences/five_star.sparql"
    ]

    for query_name in queries:
        execute_sparql_query(query_name=query_name, infer=True, format='POST')
