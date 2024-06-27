def execute_sparql_query(rdf_graph, sparql_query):
    results = rdf_graph.query(sparql_query)
    return results
