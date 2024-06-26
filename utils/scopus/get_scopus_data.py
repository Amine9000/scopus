import requests
from fastapi import HTTPException
from .scpous_api_key import SCOPUS_API_KEY


def get_scopus_data(doi):
    url = f'https://api.elsevier.com/content/abstract/doi/{doi}'
    headers = {'X-ELS-APIKey': SCOPUS_API_KEY, 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching data from Scopus API"+response.text)
