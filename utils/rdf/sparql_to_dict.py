from rdflib.plugins.sparql.processor import SPARQLResult
from pprintjson import pprintjson as ppjson


def sparql_result_to_dict(sparql_result: SPARQLResult) -> list:
    """
    Convert SPARQLResult to a list of dictionaries.
    """
    results_list = []
    for row in sparql_result:
        result_dict = {}
        for var in sparql_result.vars:
            result_dict[str(var)] = str(row[var]) if row[var] else None
        results_list.append(result_dict)
    # ppjson(results_list)
    return results_list
