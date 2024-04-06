from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings
from rdflib import Graph, URIRef, Literal

from app.models import Wizard, Skill

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)


def get_skill_info(skill_uri):
    sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>
    DESCRIBE <{skill_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

    skill_attrs = {}
    for s, p, o in g.triples((URIRef(skill_uri), None, None)):
        prop = p.split('#')[-1]
        print(s, p, o)
        if isinstance(o, Literal):
            value = o.toPython()
        else:
            value = str(o)
        skill_attrs[prop] = value

    return Skill(**skill_attrs)


def get_wizard_info(wizard_id):
    sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
    wizard_uri = f"http://hogwarts.edu/wizards/{wizard_id}"
    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>
    DESCRIBE <{wizard_uri}>
    """
    sparql.setQuery(query)
    sparql.setReturnFormat('turtle')
    results = sparql.query().convert()

    g = Graph()
    g.parse(data=results, format='turtle')

    wizard_attrs = {'id': wizard_id, 'skills': [], 'spells': []}
    for s, p, o in g:
        prop = p.split('#')[-1]
        if prop == 'has_skill':
            skill_info = get_skill_info(str(o))
            wizard_attrs['skills'].append(skill_info)
        elif prop == 'has_spell':
            # Process spells similarly if you have a Spell class
            pass
        else:
            if isinstance(o, Literal):
                value = o.toPython()
            else:
                value = str(o)
            wizard_attrs[prop] = value

    wizard = Wizard(**wizard_attrs)
    return wizard