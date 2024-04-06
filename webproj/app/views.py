from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings


# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def wizard_detail(request, wizard_id):
    sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
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

        # Handle object properties differently, assuming skills are identified by their URIs
        if prop == "has_skill":
            skill_id = val.split('/')[-1]
            wizard_data['skills'].append(skill_id)
        else:
            wizard_data[prop] = val

    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})