from fastapi import HTTPException
import requests
from .scpous_api_key import SCOPUS_API_KEY

# Define the API key and base URL
BASE_URL = 'https://api.elsevier.com/content/search/scopus'


def author_search(author_id=None, author_name=None):
    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': SCOPUS_API_KEY
    }

    # Construct the query string
    author_query = ""
    if author_id:
        author_query = f"AU-ID({author_id})"
    elif author_name:
        names = author_name.split(',')
        if len(names) == 2:
            lname, fname = names
            author_query = f"AUTHLASTNAME({lname.strip()}) AND AUTHFIRST({fname.strip()})"
        else:
            author_query = f"AUTHLASTNAME({author_name.strip()}) OR AUTHFIRST({author_name.strip()})"

    params = {
        'query': f"{author_query}",
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching data from Scopus API: " + response.text)


def author_search_pagination(start: int = 0, author_id=None, author_name=None):
    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': SCOPUS_API_KEY
    }

    author_query = ""
    if author_id:
        author_query = f"AU-ID({author_id})"
    elif author_name:
        author_query = f"AUTH({author_name})"

    params = {
        'query': f"{author_query}",
        'start': start,
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching data from Scopus API: " + response.text)
