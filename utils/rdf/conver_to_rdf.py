from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, FOAF, XSD


def convert_to_rdf(scopus_data, author_id: str):
    g = Graph()

    """
        "Author_id": author_id,
        "Nombre_total_publication": total_publications,
        "Nombre_total_citation": int(data_df['citedby-count'].sum()),
        "Average_citations": float(data_df['citedby-count'].mean()),
        "Top_publications": top_3_publications_list,
        "Distribution_citations": base64.b64encode(buf.getvalue()).decode('utf-8')

    """

    # Define namespaces
    scopus_ns = Namespace(
        "https://api.elsevier.com/content/abstract/scopus_id/")
    pub_ns = Namespace("https://www.scopus.com/sourceid/")
    g.bind('scopus', scopus_ns)

    # Example conversion for author data
    author_uri = scopus_ns[scopus_data.get("prism:url", "")]
    g.add((author_uri, RDF.type, FOAF.Person))
    g.add((author_uri, scopus_ns["authorID"], Literal(
        scopus_data.get("Author_id", 'None'), datatype=XSD.string)))
    g.add((author_uri, scopus_ns["NombreTotalPublication"], Literal(
        scopus_data.get("Nombre_total_publication", 'None'), datatype=XSD.string)))
    g.add((author_uri, scopus_ns["NombreTotalCitation"], Literal(
        scopus_data.get("Nombre_total_citation", 'None'), datatype=XSD.string)))

    for i, top_pub in enumerate(scopus_data.get("Top_publications", [])):
        pub_uri = pub_ns[top_pub.get("source-id", "")]
        g.add((author_uri, scopus_ns["hasTopPublication"], pub_uri))
        g.add((pub_uri, RDF.type, pub_ns.Publication))
        g.add((pub_uri, pub_ns.title, Literal(
            top_pub.get("dc:title", ""), datatype=XSD.string)))
        g.add((pub_uri, pub_ns.citedbyCount, Literal(
            top_pub.get("citedby-count", ""), datatype=XSD.string)))
        g.add((pub_uri, pub_ns.publicationName, Literal(
            top_pub.get("prism:publicationName", ""), datatype=XSD.string)))
        g.add((pub_uri, pub_ns.doi, Literal(
            top_pub.get("prism:doi", ""), datatype=XSD.string)))

    g.serialize(destination='scopus_data.ttl', format='turtle')

    return g
