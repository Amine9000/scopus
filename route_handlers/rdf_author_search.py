from fastapi.responses import JSONResponse
from utils.scopus.author_search import author_search
from utils.rdf.conver_to_rdf import convert_to_rdf
from utils.rdf.execute_sparql import execute_sparql_query
from utils.rdf.sparql_to_dict import sparql_result_to_dict
from route_handlers.author_search import process_data


def rdf_author_search(author_id: str = None, author_name: str = None):
    res = author_search(author_id, author_name)
    scopus_data = process_data(res, author_id=author_id)
    g = convert_to_rdf(scopus_data, author_id)
    sparql_query = """
    PREFIX scopus: <https://api.elsevier.com/content/abstract/scopus_id/>
    PREFIX pub: <https://www.scopus.com/sourceid/>

    SELECT ?id ?NombreTotalPublication ?NombreTotalCitation (GROUP_CONCAT(DISTINCT ?publication; SEPARATOR=", ") AS ?publications) (GROUP_CONCAT(DISTINCT ?pubTitle; SEPARATOR=", ") AS ?pubTitles) (GROUP_CONCAT(DISTINCT ?pubCitedbyCount; SEPARATOR=", ") AS ?pubCitedbyCounts) (GROUP_CONCAT(DISTINCT ?pubPublicationName; SEPARATOR=", ") AS ?pubPublicationNames) (GROUP_CONCAT(DISTINCT ?pubDOI; SEPARATOR=", ") AS ?pubDOIs)
    WHERE {
        ?author scopus:authorID ?id ;
                scopus:NombreTotalPublication ?NombreTotalPublication ;
                scopus:NombreTotalCitation ?NombreTotalCitation ;
                scopus:hasTopPublication ?publication .

        ?publication a pub:Publication ;
                    pub:title ?pubTitle ;
                    pub:citedbyCount ?pubCitedbyCount ;
                    pub:publicationName ?pubPublicationName ;
                    pub:doi ?pubDOI .
    }
    GROUP BY ?id ?NombreTotalPublication ?NombreTotalCitation
    """
    response_content = sparql_result_to_dict(
        execute_sparql_query(g, sparql_query))
    return JSONResponse(content=response_content)
