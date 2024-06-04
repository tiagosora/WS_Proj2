from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, Graph, URIRef, Literal
import time

ONTOLOGY_NAMESPACE = "http://hogwarts.edu/ontology.owl#"
ONTOLOGY_FILE = "../updated_ontology.owl"
DELAY = 5  # Delay in seconds between requests
RETRIES = 3  # Number of retries for failed requests

def load_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")
    return g

def get_existing_resources_and_names(g, class_name):
    resources = []
    for s, p, o in g.triples((None, RDF.type, URIRef(ONTOLOGY_NAMESPACE + class_name))):
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasName"), None)):
            resources.append((str(s), str(name)))
        for _, _, name in g.triples((s, URIRef(ONTOLOGY_NAMESPACE + "hasIncantation"), None)):
            resources.append((str(s), str(name)))
    return resources

def generate_wikidata_queries(resources):
    queries = []
    for (source, resource_name) in resources:
        query = f"""
        SELECT ?spell ?p ?pLabel ?o ?oLabel
        WHERE {{
        ?spell wdt:P31 wd:Q28872880 .
        ?spell rdfs:label ?label ;
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
        "http://www.wikidata.org/prop/direct/P361": namespace + "partOf",
        "http://www.wikidata.org/prop/direct/P366": namespace + "hasUse",
        "http://www.wikidata.org/prop/direct/P1536": namespace + "causeOf",
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

def save_graph(graph):
    graph.serialize(destination="./output_spells.owl", format='xml')

# Load existing ontology
print("Loading ontology...")
ontology_graph = load_ontology(ONTOLOGY_FILE)

# Get existing resources and their names for the class "Spell"
print("Retrieving existing resources...")
resources = get_existing_resources_and_names(ontology_graph, "Spell")

# Generate SPARQL queries for Wikidata
print("Generating Wikidata queries...")
wikidata_queries = generate_wikidata_queries(resources)

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

# Save the updated ontology back to the ontology.owl file
print("Saving updated ontology...")
save_graph(merged_graph)

print("Ontology has been updated with data from Wikidata.")
