from thefuzz.process import extract
from thefuzz.fuzz import token_sort_ratio
import re

SCORE_THRESHOLD = 50


def fuzzy_search(text, query):
    tokens = re.sub(r"\b\w{1,3}\b", "", text).split()
    scores = []
    query_tokens = query.split()
    for q in query_tokens:
        scores.extend(extract(q, tokens, limit=1, scorer=token_sort_ratio))
    if len(scores) <= 0 or scores[0][1] <= SCORE_THRESHOLD:
        return None
    matches = list(map(lambda tup: tup[0], scores))
    return " ".join(matches[: len(query_tokens)])


def clean_encode_query(query):
    return re.sub(r"[^\w]", " ", query).strip().replace(" ", "%20")
