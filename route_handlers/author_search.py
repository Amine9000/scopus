
from utils.scopus.author_search import author_search, author_search_pagination
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def process_data(data: str, author_id: str):

    entries = data.get("search-results", {}).get("entry", [])
    if len(entries) == 1:
        if "error" in entries[0]:
            print(":In")
            return {"message": entries[0]['error']}
    total_publications = int(data.get(
        "search-results", {}).get("opensearch:totalResults", 0))
    data = data.get("search-results", {}).get("entry", [])

    start = len(data)

    while start < total_publications:
        response = author_search_pagination(
            start=start, author_id=author_id)
        new_enties = response.get("search-results", {}).get("entry", [])
        data = data + new_enties
        start += len(new_enties)

    data_df = pd.DataFrame(data)
    if 'citedby-count' in data_df:
        data_df['citedby-count'] = data_df['citedby-count'].fillna(
            0).astype(int)
    else:
        data_df['citedby-count'] = 0

    data_df['prism:doi'] = data_df['prism:doi'].fillna("N/A")

    nbr_citation_total = 0
    for entry in data:
        nbr_citations = int(entry.get("citedby-count", 0))
        nbr_citation_total += nbr_citations

    top_3_publications = data_df.nlargest(3, 'citedby-count')
    top_3_publications_list = top_3_publications[[
        'dc:title', 'prism:publicationName', 'prism:doi', 'citedby-count']].to_dict(orient='records')

    distribution_of_citation = data_df[[
        'prism:doi', 'citedby-count']]

    fig, ax = plt.subplots(figsize=(15, 10))
    distribution_of_citation.plot(
        kind="bar", x='prism:doi', y='citedby-count', ax=ax)

    ax.set_xlabel('DOI')
    ax.set_ylabel('Number of Citations')
    ax.set_title('Citations per Publication')
    plt.xticks(rotation=30, ha='right')
    plt.subplots_adjust(bottom=0.3)
    plt.show()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    response_content = {
        "Author_id": author_id,
        "Nombre_total_publication": total_publications,
        "Nombre_total_citation": int(data_df['citedby-count'].sum()),
        "Average_citations": float(data_df['citedby-count'].mean()),
        "Top_publications": top_3_publications_list,
        "Distribution_citations": base64.b64encode(buf.getvalue()).decode('utf-8')
    }
    return response_content


def author_search_handler(author_id: str = None, author_name: str = None):
    print(author_name)
    res = author_search(author_id, author_name)
    response_content = process_data(res, author_id)
    return JSONResponse(content=response_content)
