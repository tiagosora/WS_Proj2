from rdflib import Graph, URIRef, RDF, OWL

def inspect_ontology(file_path):
    # Load the ontology
    g = Graph()
    g.parse(file_path, format="xml")

    # Extract and print namespaces
    namespaces = list(g.namespace_manager.namespaces())
    print("Namespaces:")
    for prefix, namespace in namespaces:
        print(f"Prefix: {prefix}, Namespace: {namespace}")

    # Extract and print classes
    print("\nClasses:")
    for s in g.subjects(predicate=RDF.type, object=OWL.Class):
        print(s)

    # Extract and print object properties
    print("\nObject Properties:")
    for s in g.subjects(predicate=RDF.type, object=OWL.ObjectProperty):
        print(s)

    # Extract and print datatype properties
    print("\nDatatype Properties:")
    for s in g.subjects(predicate=RDF.type, object=OWL.DatatypeProperty):
        print(s)

# Specify the path to your ontology file
file_path = "./updated_ontology.owl"

# Inspect the ontology
inspect_ontology(file_path)
