import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi.responses import JSONResponse
from utils.scopus.search_scopus import search_scopus
from io import BytesIO
import base64
from collections import defaultdict


def get_publication_trend(query: str):

    publication_years = []
    year = 1990
    while year <= 2024:
        data = search_scopus(query, count=25, year=year)
        if data:
            entries = data.get('search-results', {}).get('entry', [])
            for entry in entries:
                publication_date = entry.get('prism:coverDate', '')
                if publication_date:
                    publication_year = publication_date[:4]
                    publication_years.append(publication_year)

        year += 5
        year = year if year < 2024 else 2024

    publication_counts = defaultdict(int)
    for y in publication_years:
        publication_counts[y] += 1

    # Convert to DataFrame
    trend_data = pd.DataFrame.from_dict(
        publication_counts, orient='index', columns=['count']).sort_index()

    # Plot the trend
    fig, ax = plt.subplots(figsize=(15, 8))
    trend_data.plot(kind='line', ax=ax, color='green',
                    alpha=0.7, label='Bar Plot')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.title('Publication Trend Over Time')

    # Save the plot to a bytes object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    response_content = {"graph": base64.b64encode(
        buf.getvalue()).decode('utf-8')}
    return JSONResponse(content=response_content)
