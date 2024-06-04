from app.triplestore.utils import execute_sparql_query


def infer_queries():
    print("infering....")

    query_name = "app/inferences/remove_all_stars.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/AdvancedStudent.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/MediumStudent.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/BasicStudent.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')

    query_name = "app/inferences/deleteTotalHousePoints.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')

    query_name = "app/inferences/inferHousePoints.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/one_star.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/two_star.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
        
    query_name = "app/inferences/three_star.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/four_star.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')
    
    query_name = "app/inferences/five_star.sparql"
    execute_sparql_query(query_name=query_name, infer=True, format='POST')