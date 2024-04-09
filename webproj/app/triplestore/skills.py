from rdflib import URIRef, Literal
from app.triplestore.utils import execute_sparql_query

from app.models import Skill


def get_skill_info(skill_uri):
    query_name = "app/queries/get_skill_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", skill_uri=skill_uri)

    skill_attrs = {}
    for s, p, o in g.triples((URIRef(skill_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        skill_attrs[prop] = value

    return Skill(**skill_attrs)
