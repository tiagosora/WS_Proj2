import time

from rdflib import RDF, Graph, Literal, URIRef
from SPARQLWrapper import JSON, SPARQLWrapper

def load_ontology(file_path):
    """
    Load RDF graph from an XML file.
    """
    g = Graph()
    g.parse(file_path, format="xml")
    return g

def get_existing_resources_and_names(g, class_name):
    """
    Retrieve existing resources and their names from the ontology graph.
    """
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
    return resources

def generate_dbpedia_queries(resources, class_name, code):
    """
    Generate SPARQL queries for DBpedia based on provided resources and class name.
    """
    queries = []
    for (source, resource_name) in resources:
        query = f"""
        SELECT ?{class_name} ?p ?o
        WHERE {{
            ?{class_name} dbo:wikiPageWikiLink dbr:{code} .
            ?{class_name} rdfs:label ?label ;
            ?p ?o .
            FILTER regex(?label, "{resource_name}", "i")
        }}
        """
        queries.append((source, query))
    return queries

def run_queries(sparql_endpoint, queries):
    """
    Execute SPARQL queries against the given endpoint.
    """
    results = []
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setReturnFormat(JSON)
    i = 1
    for (source, query) in queries:
        print(f"Running query {i}/{len(queries)}...")
        i += 1
        success = False
        
        for _ in range(RETRIES):
            try:
                sparql.setQuery(query)
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
    """
    Process query results into a standardized format.
    """
    prop_mapping = {}
    processed_data = []
    for results_dict in results_list:
        source = results_dict["source"]
        results = results_dict["results"]
        for result in results:
            prop = result.get("p", {}).get("value")
            value = result.get("oLabel", {}).get("value")
            if prop and value and prop in prop_mapping.keys():
                processed_data.append((source, prop, value))
    return processed_data

def create_rdf_graph(processed_data):
    """
    Create an RDF graph from processed data.
    """
    g = Graph()
    for subject, predicate, obj in processed_data:
        g.add((URIRef(subject), URIRef(predicate), Literal(obj)))
    return g

def merge_graphs(base_graph, new_graph):
    """
    Merge a new RDF graph into an existing RDF graph.
    """
    for stmt in new_graph:
        base_graph.add(stmt)
    return base_graph

def save_graph(graph, destination):
    """
    Serialize RDF graph to an XML file.
    """
    graph.serialize(destination, format='xml')

# Configuration constants
ONTOLOGY_NAMESPACE = "http://hogwarts.edu/ontology.owl#"
DELAY = 5  # Delay in seconds between requests
RETRIES = 3  # Number of retries for failed requests

# File paths
input_file = "../updated_ontology.owl"
output_file = "../dbpedia_completed_ontology.owl"

# Define the classes and their corresponding DBpedia types
classes_data = [
    ("Course", "Magic_in_Harry_Potter"),
    ("House", "Hogwarts_Houses"),
    ("School", "Hogwarts"),
    ("Spell", "Magic_in_Harry_Potter"),
    ("Wizard", "List_of_supporting_Harry_Potter_characters")
]

# SPARQL endpoint URLs
DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"

# Main script
for (class_name, code) in classes_data:
    print(f"Integrating data for class: {class_name}")
    
    # Load existing ontology
    print("Loading ontology...")
    ontology_graph = load_ontology(input_file)

    # Get existing resources and their names for the class
    print("Retrieving existing resources...")
    resources = get_existing_resources_and_names(ontology_graph, class_name)
    
    # Generate SPARQL queries for DBpedia
    print("Generating DBpedia queries...")
    dbpedia_queries = generate_dbpedia_queries(resources, class_name, code)

    # Run DBpedia queries
    print("Running DBpedia queries...")
    dbpedia_results = run_queries(DBPEDIA_ENDPOINT, dbpedia_queries)
    
    # Process DBpedia results
    print("Processing DBpedia results...")
    processed_dbpedia_data = process_results(dbpedia_results, ONTOLOGY_NAMESPACE)

    # Create RDF graph from DBpedia processed data
    print("Creating RDF graph from DBpedia processed data...")
    dbpedia_graph = create_rdf_graph(processed_dbpedia_data)

    # Merge DBpedia graph into ontology
    print("Merging DBpedia data into the ontology...")
    merged_graph = merge_graphs(ontology_graph, dbpedia_graph)

    # Save the updated RDF graph
    print("Saving updated RDF graph...")
    save_graph(merged_graph, output_file)
    
    print(f"Ontology has been updated with data from DBpedia for class: {class_name}")

    # Update input file for the next iteration
    input_file = output_file

print("Integration process completed.")
