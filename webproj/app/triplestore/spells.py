from rdflib import URIRef, Literal
from app.triplestore.utils import execute_sparql_query

from app.models import Spell


def manage_spells_list(spells_uri):
    spells = []
    for spell in spells_uri:
        spells.append(get_spell_info(spell).info())

    return spells


def get_spell_info(spell_uri):
    query_name = "app/queries/get_user_info.sparql"

    results, g = execute_sparql_query(query_name, format="turtle", user_uri=spell_uri)

    spell_attrs = {'teaches_spell': []}
    for s, p, o in g.triples((URIRef(spell_uri), None, None)):
        prop = p.split('#')[-1]
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        spell_attrs[prop] = value.replace("\xa0", " ")

    spell = Spell(**spell_attrs)

    return spell
