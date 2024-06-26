from utils.scopus.get_scopus_data import get_scopus_data
from fastapi.responses import JSONResponse


def get_citations(doi: str):
    data = get_scopus_data(doi)
    citations = data.get('abstracts-retrieval-response', {}
                         ).get('coredata', {}).get('citedby-count', 0)
    return JSONResponse(content={"doi": doi, "citations": citations})
