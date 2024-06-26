from fastapi import Response
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from utils.scopus.get_scopus_data import get_scopus_data
from utils.scopus.search_scopus import search_scopus
from pprintjson import pprintjson as ppjson


def get_publication_citation(query: str):

    start = 0

    publication_years = []
    year = 2000
    citation_counts = []
    eids = []
    while start <= 2:
        start += 1
        data = search_scopus(query, start=start, count=25, year=year)

        if data:
            entries = data.get('search-results', {}).get('entry', [])
            for entry in entries:
                ppjson(entry)
                citations = int(entry.get('citedby-count', 0))
                eid = entry.get('eid', 0)
                citation_counts.append(citations)
                eids.append(eid)

    citation_data = pd.DataFrame(
        {'eid': eids, 'citations': citation_counts})

    fig, ax = plt.subplots(figsize=(15, 10))

    citation_data.plot(kind='bar', x='eid', y='citations', width=0.8, ax=ax)

    ax.set_xlabel('EID')
    ax.set_ylabel('Number of Citations')
    ax.set_title('Citations per Publication')

    plt.subplots_adjust(bottom=0.2)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type='image/png')
