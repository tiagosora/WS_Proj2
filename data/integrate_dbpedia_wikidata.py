from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, RDF, OWL
import time

# Define namespaces and prefixes for your ontology
ONTOLOGY_NAMESPACE = "http://hogwarts.edu/ontology.owl#"
ONTOLOGY_FILE = "updated_ontology.owl"
DELAY = 5  # Delay in seconds between requests
RETRIES = 3  # Number of retries for failed requests

def load_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")
    return g

def get_classes_and_properties(g):
    classes = {str(cls) for cls in g.subjects(predicate=RDF.type, object=OWL.Class)}
    obj_properties = {str(prop) for prop in g.subjects(predicate=RDF.type, object=OWL.ObjectProperty)}
    data_properties = {str(prop) for prop in g.subjects(predicate=RDF.type, object=OWL.DatatypeProperty)}
    return classes, obj_properties, data_properties

def generate_dbpedia_queries(classes, obj_properties, data_properties):
    queries = []
    for cls in classes:
        class_name = cls.split("#")[-1]
        query = f"""
        SELECT ?entity ?property ?value
        WHERE {{
          ?entity a dbo:{class_name} .
          ?entity ?property ?value .
        }}
        """
        queries.append(query)
    return queries

def generate_wikidata_queries(classes, obj_properties, data_properties):
    queries = []
    for cls in classes:
        class_name = cls.split("#")[-1]
        query = f"""
        SELECT ?entity ?property ?value
        WHERE {{
          ?entity wdt:P31 wd:Q{class_name} .
          ?entity ?property ?value .
        }}
        """
        queries.append(query)
    return queries

def run_queries(sparql_endpoint, queries):
    results = []
    sparql = SPARQLWrapper(sparql_endpoint)
    for query in queries:
        success = False
        for _ in range(RETRIES):
            try:
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                query_results = sparql.query().convert()
                results.extend(query_results["results"]["bindings"])
                success = True
                break
            except Exception as e:
                print(f"Error: {e}. Retrying in {DELAY} seconds...")
                time.sleep(DELAY)
        if not success:
            print(f"Failed to retrieve results after {RETRIES} attempts.")
    return results

def process_results(results, namespace):
    processed_data = []
    for result in results:
        entity = result.get("entity", {}).get("value")
        property = result.get("property", {}).get("value")
        value = result.get("value", {}).get("value")
        if entity and property and value:
            processed_data.append((entity, property.replace("http://dbpedia.org/ontology/", namespace), value))
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
    graph.serialize(destination="./output.owl", format='xml')

# Load existing ontology
print("Loading ontology...")
ontology_graph = load_ontology(ONTOLOGY_FILE)

# Get all classes and properties
print("Extracting classes and properties...")
classes, obj_properties, data_properties = get_classes_and_properties(ontology_graph)

# Generate SPARQL queries for DBpedia and Wikidata
print("Generating queries...")
dbpedia_queries = generate_dbpedia_queries(classes, obj_properties, data_properties)
wikidata_queries = generate_wikidata_queries(classes, obj_properties, data_properties)

# Run the queries
print("Running queries...")
dbpedia_results = run_queries("http://dbpedia.org/sparql", dbpedia_queries)
wikidata_results = run_queries("https://query.wikidata.org/sparql", wikidata_queries)

# Process the results
print("Processing results...")
processed_dbpedia_data = process_results(dbpedia_results, ONTOLOGY_NAMESPACE)
processed_wikidata_data = process_results(wikidata_results, ONTOLOGY_NAMESPACE)

# Create RDF graphs from the fetched data
print("Creating RDF graphs...")
dbpedia_graph = create_rdf_graph(processed_dbpedia_data)
wikidata_graph = create_rdf_graph(processed_wikidata_data)

# Merge the new data into the existing ontology
print("Merging graphs...")
merged_graph = merge_graphs(ontology_graph, dbpedia_graph)
merged_graph = merge_graphs(merged_graph, wikidata_graph)

# Save the updated ontology back to the ontology.owl file
print("Saving updated ontology...")
save_graph(merged_graph)

