from utils.scopus.author_search import author_search
from utils.rdf.conver_to_rdf import convert_to_rdf
from utils.rdf.execute_sparql import execute_sparql_query


def rdf_author_search(author_id: str = None, author_name: str = None):
    res = author_search(author_id, author_name)
    g = convert_to_rdf(res)
    sparql_query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT ?author WHERE {
        ?author a foaf:Person .
    }
    """
    return execute_sparql_query(rdf_graph, sparql_query)
