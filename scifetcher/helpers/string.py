from thefuzz.process import extract
from thefuzz.fuzz import token_sort_ratio
import re

SCORE_THRESHOLD = 50

def fuzzy_search(text, query):
    tokens = re.sub(r'\b\w{1,3}\b', '', text).split()
    scores = []
    for q in query.split():
        scores.extend(extract(q, tokens, limit=2, scorer=token_sort_ratio))
    scores = sorted(scores, key=lambda tup: tup[1], reverse=True)
    if scores[0][1] <= SCORE_THRESHOLD:
        return None
    return list(map(lambda tup: tup[0], scores))
