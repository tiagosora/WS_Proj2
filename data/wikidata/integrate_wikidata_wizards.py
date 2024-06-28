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
    return resources

def generate_wikidata_queries(resources):
    queries = []
    for (source, resource_name) in resources:
        query = f"""
        SELECT ?wizard ?p ?pLabel ?o ?oLabel
        WHERE {{
            ?wizard wdt:P31 wd:Q15298259 .
            ?wizard wdt:P1559 ?name ;
                ?p ?o .
            FILTER regex(?name, "{resource_name}", "i")  
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
        "http://www.wikidata.org/prop/direct/P69": namespace + "educatedAt",
        "http://www.wikidata.org/prop/direct/P551": namespace + "residentOf",
        "http://www.wikidata.org/prop/direct/P937": namespace + "workLocation",
        "http://www.wikidata.org/prop/direct/P3828": namespace + "wears",
        "http://www.wikidata.org/prop/direct/P463": namespace + "memberOf",
        "http://www.wikidata.org/prop/direct/P1038": namespace + "relative",
        "http://www.wikidata.org/prop/direct/P27": namespace + "citizebnship",
        "http://www.wikidata.org/prop/direct/P18": namespace + "image",
        "http://www.wikidata.org/prop/direct/P569": namespace + "birthDate",
        "http://www.wikidata.org/prop/direct/P19": namespace + "birthPlace",
        "http://www.wikidata.org/prop/direct/P106": namespace + "occupation",
        "http://www.wikidata.org/prop/direct/P69": namespace + "education",
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

def save_graph(graph):
    graph.serialize(destination="./output_wizards.owl", format='xml')

# Load existing ontology
print("Loading ontology...")
ontology_graph = load_ontology(ONTOLOGY_FILE)

# Get existing resources and their names for the class "Wizard"
print("Retrieving existing resources...")
resources = get_existing_resources_and_names(ontology_graph, "Wizard")

# Generate SPARQL queries for Wikidata
print("Generating Wikidata queries...")
wikidata_queries = generate_wikidata_queries(resources)

# Run the queries
print("Running Wikidata queries...")
wikidata_results = run_queries("https://query.wikidata.org/sparql", wikidata_queries)

# print("Wikidata results:")
# for result in wikidata_results:
#     print(result)

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
