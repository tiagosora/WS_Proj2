from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings


# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def wizard_detail(request, wizard_id):
    sparql = SPARQLWrapper(settings.GRAPHDB_ENDPOINT)
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

    return render(request, 'app/wizard_detail.html', {'wizard': wizard_data, 'wizard_id': wizard_id})

