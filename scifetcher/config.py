import os

ENV_CONFIG = {
    "INCLUDE_GBIF_SEARCH": os.getenv("INCLUDE_GBIF_SEARCH") == "True",
    "AUTO_SEARCH_SIMILAR_SPECIES": os.getenv("AUTO_SEARCH_SIMILAR_SPECIES") == "True",
}
