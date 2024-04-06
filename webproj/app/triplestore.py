from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings

sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)

def get_wizard_info(wizard_id):
    wizard_uri = f"http://hogwarts.edu/wizards/{wizard_id}"

    query = f"""
    PREFIX hogwarts: <http://hogwarts.edu/>

    SELECT ?property ?value WHERE {{
        <{wizard_uri}> ?property ?value .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wizard_data = {'skills': []}
    for result in results["results"]["bindings"]:
        prop = result["property"]["value"].split('/')[-1]
        val = result["value"]["value"]

        if prop == "has_skill":
            skill_id = val.split('/')[-1]
            wizard_data['skills'].append(skill_id)
        else:
            wizard_data[prop] = val
            
    return wizard_data