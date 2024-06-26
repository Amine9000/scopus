import requests
from fastapi import Response


def search_by_doi(query: str):
    # Endpoint for Scopus Abstract Retrieval API
    search_url = f'https://api.elsevier.com/content/abstract/doi/{query}'

    # Headers with API key
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    # Make the request to the Scopus API
    response = requests.get(search_url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        # Process and return the data as needed
        return JSONResponse(content=data)
    else:
        raise HTTPException(status_code=response.status_code,
                            detail=f'Error fetching data: {response.status_code}')
