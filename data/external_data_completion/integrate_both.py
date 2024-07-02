import time
from urllib.error import HTTPError
from rdflib import RDF, Graph, Literal, URIRef
from SPARQLWrapper import JSON, SPARQLWrapper

# Load ontology from a given file path
def load_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")
    return g

# Retrieve existing resources and their names from the ontology graph
def get_existing_resources_and_names(g, class_name):
    property_mapping = {
        "Course": "hasCourseName",
        "House": "hasHouseName",
        "School": "hasSchoolName",
        "Wizard": "hasName",
        "Spell": "hasIncantation"
    }
    
    resources = []
    if class_name in property_mapping:
        property_uri = URIRef(ONTOLOGY_NAMESPACE + property_mapping[class_name])
        for s, _, o in g.triples((None, property_uri, None)):
            resources.append((str(s), str(o)))
    return resources

# Generate SPARQL queries for DBpedia based on provided resources and class name
def generate_dbpedia_queries(resources, class_name, code):
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

# Generate SPARQL queries for Wikidata based on provided resources and class name
def generate_wikidata_queries(resources, class_name, code):
    queries = []
    for (source, resource_name) in resources:
        query = f"""
        SELECT ?{class_name} ?p ?pLabel ?o ?oLabel
        WHERE {{
        ?{class_name} wdt:P31 wd:{code} .
        ?{class_name} skos:altLabel ?label ;
            ?p ?o .
        FILTER regex(?label, "{resource_name}", "i")  
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """
        queries.append((source, query))
    return queries

# Execute SPARQL queries against the given endpoint
def run_queries(sparql_endpoint, queries):
    results = []
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.agent = "Mozilla/5.0"
    i = 1
    for (source, query) in queries:
        print(f"Running query {i}/{len(queries)}...")
        i += 1
        success = False
        
        for attempt in range(RETRIES):
            try:
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                query_results = sparql.query().convert()
                results.append({"source": source, "results": query_results["results"]["bindings"]})
                success = True
                break
            except HTTPError as e:
                if e.code == 403:
                    print(f"HTTP Error 403: Forbidden. Retrying in {DELAY * (attempt + 1)} seconds...")
                    time.sleep(DELAY * (attempt + 1))  # Exponential backoff
                else:
                    print(f"Error: {e}. Retrying in {DELAY} seconds...")
                    time.sleep(DELAY)
            except Exception as e:
                print(f"Unexpected Error: {e}. Retrying in {DELAY} seconds...")
                time.sleep(DELAY)
        if not success:
            print(f"Failed to retrieve results after {RETRIES} attempts.")
            
    return results

# Process DBpedia query results into a standardized format
def process_dbpedia_results(results_list, namespace):
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

# Process Wikidata query results into a standardized format
def process_wikidata_results(results_list, namespace):
    processed_data = []
    prop_mapping = {
        # Wikidata properties
        # Course
        "http://www.wikidata.org/prop/direct/P3095": namespace + "participatedBy",
        "http://www.wikidata.org/prop/direct/P2578": namespace + "isTheStudyOf",
        
        # House
        "http://www.wikidata.org/prop/direct/P361": namespace + "partOf",
        "http://www.wikidata.org/prop/direct/P138": namespace + "namedAfter",
        "http://www.wikidata.org/prop/direct/P112": namespace + "foundedBy",
        "http://www.wikidata.org/prop/direct/P94": namespace + "coatOfArms",
        "http://www.wikidata.org/prop/direct/P6364": namespace + "officialColor",
        "http://www.wikidata.org/prop/direct/P527": namespace + "hasParts",
        
        # School
        "http://www.wikidata.org/prop/direct/P571": namespace + "inception",
        "http://www.wikidata.org/prop/direct/P18": namespace + "image",
        "http://www.wikidata.org/prop/direct/P1448": namespace + "officialName",
        "http://www.wikidata.org/prop/direct/P1705": namespace + "nativeName",
        "http://www.wikidata.org/prop/direct/P1416": namespace + "affiliation",
        "http://www.wikidata.org/prop/direct/P112": namespace + "foundedBy",
        
        # Spell
        "http://www.wikidata.org/prop/direct/P361": namespace + "partOf",
        "http://www.wikidata.org/prop/direct/P366": namespace + "hasUse",
        "http://www.wikidata.org/prop/direct/P1536": namespace + "causeOf",
        
        # Wizard
        "http://www.wikidata.org/prop/direct/P69": namespace + "educatedAt",
        "http://www.wikidata.org/prop/direct/P551": namespace + "residentOf",
        "http://www.wikidata.org/prop/direct/P937": namespace + "workLocation",
        "http://www.wikidata.org/prop/direct/P3828": namespace + "wears",
        "http://www.wikidata.org/prop/direct/P463": namespace + "memberOf",
        "http://www.wikidata.org/prop/direct/P1038": namespace + "relative",
        "http://www.wikidata.org/prop/direct/P27": namespace + "citizenship",
        "http://www.wikidata.org/prop/direct/P18": namespace + "image",
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
            prop = result.get("p", {}).get("value")
            value = result.get("oLabel", {}).get("value")
            
            if prop and value and prop in prop_mapping.keys():
                mapped_prop = prop_mapping[prop]
                processed_data.append((source, mapped_prop, value))
                    
    return processed_data

# Create an RDF graph from processed data
def create_rdf_graph(processed_data):
    g = Graph()
    for subject, predicate, obj in processed_data:
        g.add((URIRef(subject), URIRef(predicate), Literal(obj)))
    return g

# Merge a new RDF graph into an existing RDF graph
def merge_graphs(base_graph, new_graph):
    for stmt in new_graph:
        base_graph.add(stmt)
    return base_graph

# Serialize RDF graph to an XML file
def save_graph(graph, destination):
    graph.serialize(destination, format='xml')

# Configuration constants
ONTOLOGY_NAMESPACE = "http://hogwarts.edu/ontology.owl#"
DELAY = 5  # Delay in seconds between requests
RETRIES = 3  # Number of retries for failed requests

# File paths
input_file = "../data.rdf"
output_file = "../completed_data.rdf"

# Define the classes and their corresponding DBpedia and Wikidata types
classes_data = [
    ("Course", "Magic_in_Harry_Potter", "Q1647221"),
    ("House", "Hogwarts_Houses", "Q933971"),
    ("School", "Hogwarts", "Q2043034"),
    ("Spell", "Magic_in_Harry_Potter", "Q28872880"),
    ("Wizard", "List_of_supporting_Harry_Potter_characters", "Q117289741")
]

# SPARQL endpoint URLs
DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

# Main script
for (class_name, dbpedia_code, wikidata_code) in classes_data:
    print(f"Integrating data for class: {class_name}")
    
    # Load existing ontology
    print("Loading ontology...")
    ontology_graph = load_ontology(input_file)

    # Get existing resources and their names for the class
    print("Retrieving existing resources...")
    resources = get_existing_resources_and_names(ontology_graph, class_name)
    
    # Generate SPARQL queries for DBpedia
    print("Generating DBpedia queries...")
    dbpedia_queries = generate_dbpedia_queries(resources, class_name, dbpedia_code)

    # Run DBpedia queries
    print("Running DBpedia queries...")
    dbpedia_results = run_queries(DBPEDIA_ENDPOINT, dbpedia_queries)
    
    # Process DBpedia results
    print("Processing DBpedia results...")
    processed_dbpedia_data = process_dbpedia_results(dbpedia_results, ONTOLOGY_NAMESPACE)

    # Create RDF graph from DBpedia processed data
    print("Creating RDF graph from DBpedia processed data...")
    dbpedia_graph = create_rdf_graph(processed_dbpedia_data)

    # Generate SPARQL queries for Wikidata
    print("Generating Wikidata queries...")
    wikidata_queries = generate_wikidata_queries(resources, class_name, wikidata_code)

    # Run Wikidata queries
    print("Running Wikidata queries...")
    wikidata_results = run_queries(WIKIDATA_ENDPOINT, wikidata_queries)

    # Process Wikidata results
    print("Processing Wikidata results...")
    processed_wikidata_data = process_wikidata_results(wikidata_results, ONTOLOGY_NAMESPACE)

    # Create RDF graph from Wikidata processed data
    print("Creating RDF graph from Wikidata processed data...")
    wikidata_graph = create_rdf_graph(processed_wikidata_data)

    # Merge DBpedia and Wikidata graphs into ontology
    print("Merging DBpedia and Wikidata data into the ontology...")
    merged_graph = merge_graphs(ontology_graph, dbpedia_graph)
    merged_graph = merge_graphs(merged_graph, wikidata_graph)

    # Save the updated RDF graph
    print("Saving updated RDF graph...")
    save_graph(merged_graph, output_file)
    
    print(f"Ontology has been updated with data from DBpedia and Wikidata for class: {class_name}")

    # Update input file for the next iteration
    input_file = output_file

print("Integration process completed.")
