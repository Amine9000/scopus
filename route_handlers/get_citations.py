from utils.scopus.get_scopus_data import get_scopus_data
from fastapi.responses import JSONResponse
from pprintjson import pprintjson as ppjson


def get_citations(doi_1: str = None, doi_2: str = None):
    data = get_scopus_data(doi_1, doi_2)
    ppjson(data)
    citations = data.get('abstracts-retrieval-response', {}
                         ).get('coredata', {}).get('citedby-count', 0)
    affiliations = data.get('abstracts-retrieval-response', {}
                            ).get("affiliation", [])
    publicationName = data.get('abstracts-retrieval-response', {}
                               ).get("coredata", {}).get("prism:publicationName", "")
    title = data.get('abstracts-retrieval-response', {}
                     ).get("coredata", {}).get("dc:title", "")

    authors = data.get('abstracts-retrieval-response', {}
                       ).get("coredata", {}).get("dc:creator", {}).get("author", [])
    author_name = ''
    if authors:
        preferred_name = authors[0].get("preferred-name", {})
        given_name = preferred_name.get("ce:given-name", '')
        surname = preferred_name.get("ce:surname", '')
        author_name = f"{given_name} {surname}".strip()

    return JSONResponse(content={"doi": doi_1+"/"+doi_2, "publicationName": publicationName, "title": title, "citations": citations, "author": author_name, "affiliations": affiliations})
