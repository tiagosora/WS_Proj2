from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings


# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def wizard_detail(request, wizard_id):
    sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
    wizard_uri = f"http://hogwarts.edu/wizards/{wizard_id}"

    # Query for wizard properties, including skill and spell URIs
    query_wizard = f"""
    PREFIX hogwarts: <http://hogwarts.edu/ontology#>

    SELECT ?property ?obj WHERE {{
        <{wizard_uri}> ?property ?obj .
    }}
    """
    sparql.setQuery(query_wizard)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wizard_data = {'skills': [], 'spells': []}
    for result in results["results"]["bindings"]:
        prop = result["property"]["value"].split('#')[-1]
        obj = result["obj"]["value"]

        if prop == "has_skill":
            query_skill = f"""
            PREFIX hogwarts: <http://hogwarts.edu/ontology#>

            SELECT ?name WHERE {{
                <{obj}> hogwarts:name ?name .
            }}
            """
            sparql.setQuery(query_skill)
            skill_results = sparql.query().convert()
            for skill_result in skill_results["results"]["bindings"]:
                skill_name = skill_result["name"]["value"]
                wizard_data['skills'].append(skill_name)

    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

