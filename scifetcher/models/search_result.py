class SearchResult:
    def __init__(self, key, query) -> None:
        self.key = key
        self.query = query
        self.species_list = []

    def append(self, species):
        self.species_list.append(species)

    def extend(self, species_list):
        self.species_list.extend(species_list)

    def set_description(self, desc):
        self.description = desc
