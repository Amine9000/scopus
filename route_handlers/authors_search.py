from route_handlers.author_search import process_data
from utils.scopus.author_search import author_search
from typing import List


def authors_search(authors: str):
    authors = authors.split(",")
    autors_data = []
    for author in authors:
        print(author)
        autors_data.append(process_data(
            author_search(author_id=author), author))
    return autors_data
