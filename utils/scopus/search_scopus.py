from fastapi import HTTPException
import requests
from .scpous_api_key import SCOPUS_API_KEY

# Define the API key and base URL
BASE_URL = 'https://api.elsevier.com/content/search/scopus'


def search_scopus(query, start=0, count=10, year=2024):
    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': SCOPUS_API_KEY
    }

    params = {
        'query': f"{query} AND PUBYEAR IS {year}",
        'start': start,
        'count': count
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching data from Scopus API: " + response.text)

# Example usage
# results = search_scopus("your search query", start=0, count=10, start_year=2000, end_year=2024)
