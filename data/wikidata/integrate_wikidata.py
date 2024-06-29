import time

from rdflib import RDF, Graph, Literal, URIRef
from SPARQLWrapper import JSON, SPARQLWrapper


def load_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")
    return g

def get_existing_resources_and_names(g, class_name):
    resources = []
    for s, _, _ in g.triples((None, RDF.type, URIRef(ONTOLOGY_NAMESPACE + class_name))):
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasCourseName"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasHouseName"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasSchoolName"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasName"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasIncantation"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasName"), None)):
            resources.append((str(s), str(name)))
    return resources

def generate_wikidata_queries(resources, class_name, code):
    queries = []
    for (source, resource_name) in resources:
        query = f"""
        SELECT ?{class_name} ?p ?pLabel ?o ?oLabel
        WHERE {{
        ?{class_name} wdt:P31 wd:{code} .
        ?{class_name} rdfs:label ?label ;
            ?p ?o .
        FILTER regex(?label, "{resource_name}", "i")  
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """
        queries.append((source, query))
    return queries

def run_queries(sparql_endpoint, queries):
    results = []
    sparql = SPARQLWrapper(sparql_endpoint)
    i = 1
    for (source, query) in queries:
        print(f"Running query {i}/{len(queries)}...")
        i += 1
        success = False
        
        for _ in range(RETRIES):
            try:
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                query_results = sparql.query().convert()
                results.append({"source": source, 
                                "results": query_results["results"]["bindings"]})
                success = True
                break
            except Exception as e:
                print(f"Error: {e}. Retrying in {DELAY} seconds...")
                time.sleep(DELAY)
        if not success:
            print(f"Failed to retrieve results after {RETRIES} attempts.")
            
    return results

def process_results(results_list, namespace):
    processed_data = []
    property_mapping = {
        # Wikidata properties
        # Houses
        "http://www.wikidata.org/prop/direct/P361": namespace + "partOf",
        "http://www.wikidata.org/prop/direct/P138": namespace + "namedAfter",
        "http://www.wikidata.org/prop/direct/P112": namespace + "foundedBy",
        "http://www.wikidata.org/prop/direct/P94": namespace + "coatOfArms",
        "http://www.wikidata.org/prop/direct/P6364": namespace + "officialColor",
        "http://www.wikidata.org/prop/direct/P527": namespace + "hasParts",
        "http://www.wikidata.org/prop/direct/P3095": namespace + "participatedBy",
        "http://www.wikidata.org/prop/direct/P2578": namespace + "isTheStudyOf",
        "http://www.wikidata.org/prop/direct/P1074": namespace + "fictionalOrMythicalAnalogOf",
        "http://www.wikidata.org/prop/direct/P571": namespace + "inception",
        "http://www.wikidata.org/prop/direct/P18": namespace + "image",
        "http://www.wikidata.org/prop/direct/P1448": namespace + "officialName",
        "http://www.wikidata.org/prop/direct/P1705": namespace + "nativeName",
        "http://www.wikidata.org/prop/direct/P1416": namespace + "affiliation",
        "http://www.wikidata.org/prop/direct/P366": namespace + "hasUse",
        "http://www.wikidata.org/prop/direct/P1536": namespace + "causeOf",
        "http://www.wikidata.org/prop/direct/P69": namespace + "educatedAt",
        "http://www.wikidata.org/prop/direct/P551": namespace + "residentOf",
        "http://www.wikidata.org/prop/direct/P937": namespace + "workLocation",
        "http://www.wikidata.org/prop/direct/P3828": namespace + "wears",
        "http://www.wikidata.org/prop/direct/P463": namespace + "memberOf",
        "http://www.wikidata.org/prop/direct/P1038": namespace + "relative",
        "http://www.wikidata.org/prop/direct/P27": namespace + "citizebnship",
        "http://www.wikidata.org/prop/direct/P569": namespace + "birthDate",
        "http://www.wikidata.org/prop/direct/P19": namespace + "birthPlace",
        "http://www.wikidata.org/prop/direct/P106": namespace + "occupation",
        "http://www.wikidata.org/prop/direct/P1476": namespace + "title",
        "http://www.wikidata.org/prop/direct/P40": namespace + "children",
        "http://www.wikidata.org/prop/direct/P22": namespace + "father",
        "http://www.wikidata.org/prop/direct/P25": namespace + "mother",
        "http://www.wikidata.org/prop/direct/P26": namespace + "spouse",
        "http://www.wikidata.org/prop/direct/P3373": namespace + "sibling",
        "http://www.wikidata.org/prop/direct/P570": namespace + "deathDate"
    }
    
    for results_dict in results_list:
        
        source = results_dict["source"]
        results = results_dict["results"]
        
        for result in results:
        
            property = result.get("p", {}).get("value")
            value = result.get("oLabel", {}).get("value")
            
            if property and value:
                if property in property_mapping.keys():
                    mapped_property = property_mapping[property]
                    processed_data.append((source, mapped_property, value))
                    
    return processed_data

def create_rdf_graph(processed_data):
    g = Graph()
    for subject, predicate, obj in processed_data:
        g.add((URIRef(subject), URIRef(predicate), Literal(obj)))
    return g

def merge_graphs(base_graph, new_graph):
    for stmt in new_graph:
        base_graph.add(stmt)
    return base_graph

def save_graph(graph, destination):
    graph.serialize(destination, format='xml')

ONTOLOGY_NAMESPACE = "http://hogwarts.edu/ontology.owl#"
DELAY = 5  # Delay in seconds between requests
RETRIES = 3  # Number of retries for failed requests
input_file = "../updated_ontology.owl"
output_file = f"../completed_ontology.owl"

classes_data = [("Course", "Q1647221"),
                ("House", "Q933971"),
                ("School", "Q2043034"),
                ("Spell", "Q28872880"),
                ("Wizard", "Q15298259")]

# Integrate data for each class
for (class_name, code) in classes_data:
    
    print(f"Integrating data for class: {class_name}")
    # Load existing ontology
    print("Loading ontology...")
    ontology_graph = load_ontology(input_file)

    # Get existing resources and their names for the class
    print("Retrieving existing resources...")
    resources = get_existing_resources_and_names(ontology_graph, class_name)
    
    # Generate SPARQL queries for Wikidata
    print("Generating Wikidata queries...")
    wikidata_queries = generate_wikidata_queries(resources, class_name, code)

    # Run the queries
    print("Running Wikidata queries...")
    wikidata_results = run_queries("https://query.wikidata.org/sparql", wikidata_queries)

    # Process the results
    print("Processing Wikidata results...")
    processed_wikidata_data = process_results(wikidata_results, ONTOLOGY_NAMESPACE)

    # Create RDF graphs from the fetched data
    print("Creating RDF graph from the processed data...")
    wikidata_graph = create_rdf_graph(processed_wikidata_data)

    # Merge the new data into the existing ontology
    print("Merging data into the ontology...")
    merged_graph = merge_graphs(ontology_graph, wikidata_graph)

    # Save the updated RDF graph
    print("Saving updated RDF graph...")
    save_graph(merged_graph, output_file)
    
    print("Ontology has been updated with data from Wikidata.")

    input_file = output_file
    
# # Initialize a list to store each graph
# graphs = []

# # List of file paths
# file_paths = [
#     "./output_courses.rdf",
#     "./output_houses.rdf",
#     "./output_schools.rdf",
#     "./output_spells.rdf",
#     "./output_wizards.rdf",
#     "../updated_ontology.rdf",
# ]

# # Load each file into a separate graph
# for file_path in file_paths:
#     g = Graph()
#     g.parse(file_path, format="xml")
#     graphs.append(g)

# # Create a new graph for the merged content
# merged_graph = Graph()

# # Merge all graphs into the merged graph
# for g in graphs:
#     merged_graph += g

# # Save the merged graph to a new file
# merged_file_path = "./final_data.rdf"
# merged_graph.serialize(destination=merged_file_path, format="xml")