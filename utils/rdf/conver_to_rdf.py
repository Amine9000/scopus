from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, FOAF, XSD
from pprintjson import pprintjson as ppjson


def convert_to_rdf(scopus_data):
    ppjson(scopus_data)
    # Initialize RDF graph
    g = Graph()

    # Define namespaces
    scopus_ns = Namespace(
        "https://api.elsevier.com/content/abstract/scopus_id/")
    g.bind('scopus', scopus_ns)

    # Example conversion for author data
    author_uri = scopus_ns[scopus_data.get("prism:url")]
    g.add((author_uri, RDF.type, FOAF.Person))
    g.add((author_uri, FOAF.name, Literal(author_name, datatype=XSD.string)))

    g.serialize(destination='scopus_data.ttl', format='turtle')

    return g
