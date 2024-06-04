from SPARQLWrapper import SPARQLWrapper, JSON
import os

sparql = SPARQLWrapper(os.getenv('REPO_URL'))

def execute_type_query(type: str, limit: int = 10):
    query = f"""
        PREFIX : <http://hogwarts.edu/ontology.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?data
        WHERE {{
            ?data rdf:type :{type} .
        }}
        LIMIT {limit}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    uris = [binding['data']['value'] for binding in results['results']['bindings']]
    
    return uris

def get_information_about_uri(uri: str):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://hogwarts.edu/ontology.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?predicate ?object
        WHERE {{
            <{uri}> ?predicate ?object .
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    uri_information = {uri: {}}
    
    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        object_value = result["object"]["value"]
        uri_information[uri][predicate] = object_value
    
    return uri_information

