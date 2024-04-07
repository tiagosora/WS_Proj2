from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET, TURTLE
from django.conf import settings

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
sparql_update = SPARQLWrapper(settings.GRAPHDB_ENDPOINT_UPDATE)

def get_wizard_info(wizard_id):

    wizard_uri = f"http://hogwarts.edu/wizards/{wizard_id}"

    # Query for wizard properties, including skill URIs
    query_wizard = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>

    SELECT ?property ?obj WHERE {{
        <{wizard_uri}> ?property ?obj .
    }}
    """
    sparql.setQuery(query_wizard)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wizard_data = {'skills': []}
    for result in results["results"]["bindings"]:
        prop = result["property"]["value"].split('#')[-1]  # Assuming the namespace ends with '#'
        obj = result["obj"]["value"]

        # Check if the property is a skill
        if prop == "has_skill":
            # Fetch the skill name based on the skill URI
            query_skill = f"""
            PREFIX hogwarts: <http://hogwarts.edu/ontology#>

            SELECT ?name WHERE {{
                <{obj}> hogwarts:name ?name .
            }}
            """
            print(query_skill)
            sparql.setQuery(query_skill)
            skill_results = sparql.query().convert()
            print(skill_results)
            for skill_result in skill_results["results"]["bindings"]:
                skill_name = skill_result["name"]["value"]
                print(skill_name)
                wizard_data['skills'].append(skill_name)
        else:
            wizard_data[prop] = obj
            
            
def create_new_wizard(password, blood_type, eye_color, gender, 
                      house, nmec, name, 
                      patronus, species, wand):
    
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
            ?house hogwarts:name ?houseName .
            FILTER(LCASE(?houseName) = LCASE("{house}")) . 
            ?house hogwarts:id ?houseId .
        }}
    """
    
    sparql.setQuery(houseId_query)
    sparql.setMethod(GET)
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
                    hogwarts:wizard <http://hogwarts.edu/wizards/{max_wizard_id}> .
        }}
        }}
    """

    print(query_add)
    
    
    sparql_update.setMethod(POST)
    sparql_update.setQuery(query_add)
    sparql_update.query()
    