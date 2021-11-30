class Species:
    def __init__(self, description):
        self.description = description

    def __init__(
        self,
        source="",
        taxonomic_status="",
        rank="",
        canonical_name="",
        authorship="",
        taxon_kingdom="",
        taxon_phylum="",
        taxon_class="",
        taxon_order="",
        taxon_family="",
        taxon_genus="",
        taxon_species="",
        description="",
        match_type="",
        match_confidence=0,
    ) -> None:
        self.source = source
        self.taxonomic_status = taxonomic_status
        self.rank = rank
        self.canonical_name = canonical_name
        self.authorship = authorship
        self.taxon_kingdom = taxon_kingdom
        self.taxon_phylum = taxon_phylum
        self.taxon_class = taxon_class
        self.taxon_order = taxon_order
        self.taxon_family = taxon_family
        self.taxon_genus = taxon_genus
        self.taxon_species = taxon_species
        self.description = description
        self.match_type = match_type
        self.match_confidence = match_confidence

    def get_taxonomy(self):
        return f"{self.taxon_kingdom} > {self.taxon_phylum} > {self.taxon_class} > {self.taxon_order} > {self.taxon_family} > {self.taxon_species}"
