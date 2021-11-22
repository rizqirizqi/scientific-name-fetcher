class BaseApi:
    def __init__(self, query) -> None:
        super().__init__()
        self.query = query

    def get_description():
        raise NotImplementedError

    def get_taxonomic_status():
        raise NotImplementedError

    def get_rank():
        raise NotImplementedError

    def get_canonical_name():
        raise NotImplementedError

    def get_authorship():
        raise NotImplementedError

    def get_kingdom():
        raise NotImplementedError

    def get_phylum():
        raise NotImplementedError

    def get_class():
        raise NotImplementedError

    def get_order():
        raise NotImplementedError

    def get_family():
        raise NotImplementedError

    def get_genus():
        raise NotImplementedError

    def get_species():
        raise NotImplementedError

    def get_taxonomy():
        raise NotImplementedError
