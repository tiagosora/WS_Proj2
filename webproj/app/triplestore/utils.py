from django.conf import settings
from rdflib import Graph
from SPARQLWrapper import JSON, POST, SPARQLWrapper

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
sparql_update = SPARQLWrapper(settings.GRAPHDB_ENDPOINT_UPDATE)


def load_sparql_query(filename, **kwargs):
    with open(filename, 'r') as file:
        query_template = file.read()

    query = query_template.format(**kwargs)
    return query


def execute_sparql_query(query_name, format="JSON", **kwargs):
    g = Graph()
    results = None

    if format == "POST":
        query = load_sparql_query(query_name, **kwargs)
        sparql_update.setMethod(POST)
        sparql_update.setQuery(query)
        sparql_update.query()

    else:
        query = load_sparql_query(query_name, **kwargs)
        sparql.setQuery(query)
        if format == 'JSON':
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
        elif format == 'turtle':
            sparql.setReturnFormat('turtle')
            results = sparql.query().convert()
            g.parse(data=results, format='turtle')

    return results, g


def check_if_nmec_exists(nmec):
    query_name = "app/queries/check_if_nmec_exists.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON", nmec=nmec)

    return bool(results["boolean"])
