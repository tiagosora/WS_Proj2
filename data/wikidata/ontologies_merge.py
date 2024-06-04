from rdflib import Graph

# Initialize a list to store each graph
graphs = []

# List of file paths
file_paths = [
    "./output_courses.owl",
    "./output_houses.owl",
    "./output_schools.owl",
    "./output_spells.owl",
    "./output_wizards.owl",
    "../updated_ontology.owl",
]

# Load each file into a separate graph
for file_path in file_paths:
    g = Graph()
    g.parse(file_path, format="xml")
    graphs.append(g)

# Create a new graph for the merged content
merged_graph = Graph()

# Merge all graphs into the merged graph
for g in graphs:
    merged_graph += g

# Save the merged graph to a new file
merged_file_path = "./merged_ontology.owl"
merged_graph.serialize(destination=merged_file_path, format="xml")

merged_file_path
