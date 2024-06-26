from utils.scopus.author_search import author_search
from typing import List


def authors_search(authors: List[str]):
    autors_data = []
    for author in authors:
        autors_data.append(author_search(author))
    return autors_data
