from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.plt.plot import generate_plot
from route_handlers.search_by_doi import search_by_doi
from route_handlers.get_citations import get_citations
from route_handlers.get_publication_trend import get_publication_trend
from route_handlers.get_publication_citaion import get_publication_citation
from route_handlers.author_search import author_search_handler
from route_handlers.authors_search import authors_search
from route_handlers.rdf_author_search import rdf_author_search

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/citations/{doi_1}/{doi_2}")
async def get_citations_route(doi_1: str = None, doi_2: str = None):
    return get_citations(doi_1, doi_2)


@app.get("/publications/trend")
async def get_publication_trend_route(query: str):
    return get_publication_trend(query)


@app.get("/publications/citations")
async def get_publication_citations_route(query: str):
    return get_publication_citation(query)


@app.get("/author")
async def get_author(author_id: str = None, author_name: str = None):
    return author_search_handler(author_id, author_name)


@app.get("/rdf/author")
async def get_rdf_author(author_id: str = None, author_name: str = None):
    return rdf_author_search(author_id, author_name)


@app.get("/authors")
async def get_authors(auth_ids):
    return rdf_author_search(auth_ids)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
