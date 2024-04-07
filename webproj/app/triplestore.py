from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET, TURTLE
from django.conf import settings
from rdflib import Graph, URIRef, Literal

from app.models import Wizard, Skill

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
sparql_update = SPARQLWrapper(settings.GRAPHDB_ENDPOINT_UPDATE)

def get_skill_info(skill_uri):
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


def create_new_wizard(password, blood_type, eye_color, gender, 
                      house, nmec, name, 
                      patronus, species, wand):
    
    if ( not bool(password) or not bool(name) or not bool(nmec)):
        return False
    
    if check_if_nmec_exists(nmec):
        return False
    
    max_wizard_id = max_student_id = max_account_id = houseId = None
    
    max_ids_query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT 
            (MAX(xsd:integer(?wizardId)) AS ?nextWizardId) 			
            (MAX(xsd:integer(?studentId)) AS ?nextStudentId)
            (MAX(xsd:integer(?accountId)) AS ?nextAccountId)
        WHERE {{
            ?wizard rdfs:type "wizard" .
            ?wizard hogwarts:id ?wizardId .
            ?student rdfs:type "student" .
            ?student hogwarts:id ?studentId .
            ?account rdfs:type "account" . 
            ?account hogwarts:id ?accountId .
        }}
    """
    
    sparql.setQuery(max_ids_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    max_wizard_id = int(results["results"]["bindings"][0]["nextWizardId"]["value"]) + 1
    max_student_id = int(results["results"]["bindings"][0]["nextStudentId"]["value"]) + 1
    max_account_id = int(results["results"]["bindings"][0]["nextAccountId"]["value"]) + 1
    
    house = house if house else ""
    
    houseId_query = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT 
            ?houseId
        WHERE {{
            ?house rdfs:type "house" .
            ?house hogwarts:name ?houseName .
            FILTER(LCASE(?houseName) = LCASE("{house}")) . 
            ?house hogwarts:id ?houseId .
        }}
    """
    
    sparql.setQuery(houseId_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"])>0 and "houseId" in results["results"]["bindings"][0].keys():
        houseId = results["results"]["bindings"][0]["houseId"]["value"]
    
    house = "hogwarts:house \"" + houseId + "\" ;" if houseId else ""
    
    name = name if name else ""
    gender = "hogwarts:gender \"" + gender + "\" ;" if gender else ""
    species = "hogwarts:species \"" + species + "\" ;" if species else ""
    blood_type = "hogwarts:blood-type \"" + blood_type + "\" ;" if blood_type else ""
    eye_color = "hogwarts:eye_color \"" + eye_color + "\" ;" if eye_color else ""
    wand = "hogwarts:wand \"" + wand + "\" ;" if wand else ""
    patronus = "hogwarts:patronus \"" + patronus + "\" ;" if patronus else ""
    
    
    query_add = f"""
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {{
        GRAPH <http://hogwarts.edu/ontology#> {{
            
                <http://hogwarts.edu/wizards/{max_wizard_id}> 
                    hogwarts:id "{max_wizard_id}" ;
                    rdfs:type "wizard" ;
                    hogwarts:name "{name}" ;
                    {gender}
                    {species}
                    {blood_type}
                    {eye_color}
                    {house}
                    {wand}
                    {patronus} .

                <http://hogwarts.edu/accounts/{max_account_id}> 
                    hogwarts:id "{max_account_id}";
                    rdfs:type "account" ;
                    hogwarts:number "{nmec}" ;
                    hogwarts:password "{password}" ;
                    hogwarts:wizard <http://hogwarts.edu/wizards/{max_wizard_id}> .


                <http://hogwarts.edu/students/{max_student_id}> 
                    hogwarts:id "{max_student_id}" ;
                    rdfs:type "student" ;
                    hogwarts:school <http://hogwarts.edu/schools/1> ;
                    hogwarts:school_year "1" ;
                    hogwarts:wizard <http://hogwarts.edu/wizards/{max_wizard_id}> .
        }}
        }}
    """    
    
    sparql_update.setMethod(POST)
    sparql_update.setQuery(query_add)
    sparql_update.query()
    
    return True
    
def check_if_nmec_exists(nmec):
    
    query_check = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>

        ASK WHERE {{
            ?student rdfs:type "account" .
            ?student hogwarts:number "{nmec}" .
        }}
    """
    
    sparql.setQuery(query_check)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    return bool(results["boolean"])

def check_authentication_correct(nmec, password):
    query_check = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX hogwarts: <http://hogwarts.edu/ontology#>

        ASK WHERE {{
            ?student rdfs:type "account" .
            ?student hogwarts:number "{nmec}" .
            ?student hogwarts:password "{password}"
        }}
    """
    
    sparql.setQuery(query_check)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    return bool(results["boolean"])