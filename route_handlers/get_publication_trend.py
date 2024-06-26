import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi import Response
from utils.scopus.search_scopus import search_scopus
from io import BytesIO
from collections import defaultdict
from pprintjson import pprintjson as ppjson


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
                    publication_year = publication_date
                    publication_years.append(publication_year)

        year += 5

    ppjson(publication_years)

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
    return Response(content=buf.getvalue(), media_type='image/png')
