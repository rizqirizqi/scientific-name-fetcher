class Species:
    def __init__(
        self,
        source="",
        taxonomic_status="",
        rank="",
        scientific_name="",
        canonical_name="",
        authorship="",
        taxon_kingdom="",
        taxon_phylum="",
        taxon_class="",
        taxon_order="",
        taxon_family="",
        taxon_genus="",
        taxon_species="",
        match_type="",
        match_confidence=0,
    ) -> None:
        self.source = source
        self.taxonomic_status = taxonomic_status
        self.rank = rank
        self.scientific_name = scientific_name
        self.canonical_name = canonical_name
        self.authorship = authorship
        self.taxon_kingdom = taxon_kingdom
        self.taxon_phylum = taxon_phylum
        self.taxon_class = taxon_class
        self.taxon_order = taxon_order
        self.taxon_family = taxon_family
        self.taxon_genus = taxon_genus
        self.taxon_species = taxon_species
        self.match_type = match_type
        self.match_confidence = match_confidence

    def get_taxonrank(self):
        return f"{self.taxon_kingdom} > {self.taxon_phylum} > {self.taxon_class} > {self.taxon_order} > {self.taxon_family} > {self.taxon_species}"

    def to_dict(self):
        return {
            "Source": self.source,
            "Status": self.taxonomic_status,
            "Rank": self.rank,
            "Scientific Name": self.scientific_name,
            "Canonical Name": self.canonical_name,
            "Authorship": self.authorship,
            "Kingdom": self.taxon_kingdom,
            "Phylum": self.taxon_phylum,
            "Class": self.taxon_class,
            "Order": self.taxon_order,
            "Family": self.taxon_family,
            "Genus": self.taxon_genus,
            "Species": self.taxon_species,
            "MatchType": self.match_type,
            "Confidence": self.match_confidence,
        }
