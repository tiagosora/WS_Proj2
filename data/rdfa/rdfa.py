import execute_queries

def initialize():
    return [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Hogwarts RDFa</title>',
        '</head>',
        '<body>',
        '    <div xmlns="http://www.w3.org/1999/xhtml"',
        '         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"',
        '         xmlns:owl="http://www.w3.org/2002/07/owl#"',
        '         xmlns:xsd="http://www.w3.org/2001/XMLSchema#"',
        '         xmlns:sp="http://spinrdf.org/sp#"',
        '         xmlns="http://hogwarts.edu/ontology#">',
        '        <div typeof="owl:Ontology">',
        '            <span property="rdfs:comment" lang="en">Hogwarts Ontology.</span>',
        '            <span property="rdfs:label" lang="en">Hogwarts Ontology</span>',
        '            <span property="owl:versionInfo">1.0</span>',
        '        </div>'
    ]

def generate_html_for_type(rdfa, type_name, limit=10):
    uris = execute_queries.execute_type_query(type_name, limit)
    
    for uri in uris:
        information = execute_queries.get_information_about_uri(uri)
        rdfa.append(f'<div typeof=":{type_name}" about="{uri}">')
        for predicate, obj in information[uri].items():
            if obj.startswith("http"):
                rdfa.append(f'    <a property="{predicate}" href="{obj}">{obj}</a>')
            else:
                rdfa.append(f'    <span property="{predicate}">{obj}</span>')
        rdfa.append(f'</div>')
    return rdfa

def main():
    rdfa = initialize()
    rdfa = generate_html_for_type(rdfa, "Account", limit=2) 
    rdfa = generate_html_for_type(rdfa, "Wizard", limit=2)  
    rdfa = generate_html_for_type(rdfa, "Professor", limit=2) 
    rdfa = generate_html_for_type(rdfa, "Headmaster", limit=2)
    rdfa = generate_html_for_type(rdfa, "Course", limit=2) 
    rdfa = generate_html_for_type(rdfa, "Spell", limit=2)
    rdfa = generate_html_for_type(rdfa, "Skills", limit=2) 
    rdfa.append('</div>')
    rdfa.append('</body>')
    rdfa.append('</html>')
    
    with open("output.html", 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(rdfa))
    

if __name__ == "__main__":
    main()
