from app.models import Spell
from app.triplestore.utils import execute_sparql_query
from rdflib import Literal, URIRef


def manage_spells_list(spells_uri):
    spells = []
    for spell in spells_uri:
        spells.append(get_spell_info(spell).info())

    return spells


def get_spell_info(spell_uri):
    query_name = "app/queries/get_entity_info_by_uri.sparql"

    _, g = execute_sparql_query(query_name, format="turtle", uri=spell_uri)

    spell_attrs = {'id': spell_uri, 'teaches_spell': []}
    for s, p, o in g.triples((URIRef(spell_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        spell_attrs[prop] = value.replace("\xa0", " ") if bool(value) else "Unknown"

    spell = Spell(**spell_attrs)

    return spell


def get_len_all_spells():
    query_name = "app/queries/get_len_all_spells.sparql"

    results, _ = execute_sparql_query(query_name, format="JSON")

    if len(results["results"]["bindings"]) > 0:
        return int(results["results"]["bindings"][0]["count"]["value"])

    return None
