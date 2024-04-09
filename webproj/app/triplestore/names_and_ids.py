from app.triplestore.utils import execute_sparql_query


def get_professor_name(professor_uri):
    query_name = "app/queries/get_professor_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", professor_uri=professor_uri)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


def get_house_name(houseId):
    query_name = "app/queries/get_house_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", houseId=houseId)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name


def get_school_name(school_uri):
    query_name = "app/queries/get_school_name.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", school_uri=school_uri)

    name = ""
    if len(results["results"]["bindings"]) > 0:
        name = results["results"]["bindings"][0]["name"]["value"]

    return name
