class Species:

    source: str
    id: str
    url: str
    search_url: str
    taxonomic_status: str
    rank: str
    accepted_name: str
    scientific_name: str
    canonical_name: str
    authorship: str
    taxon_kingdom: str
    taxon_phylum: str
    taxon_class: str
    taxon_order: str
    taxon_family: str
    taxon_genus: str
    taxon_species: str
    threat_status: str
    match_type: str
    match_confidence: int

    def __init__(
        self,
        source="",
        id=None,
        url="",
        search_url="",
        taxonomic_status="",
        rank="",
        accepted_name="",
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
        threat_status="",
        match_type="",
        match_confidence=0,
    ) -> None:
        self.source = source
        self.id = id
        self.url = url
        self.search_url = search_url
        self.taxonomic_status = taxonomic_status
        self.rank = rank
        self.accepted_name = accepted_name
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
        self.threat_status = threat_status
        self.match_type = match_type
        self.match_confidence = match_confidence

    def get_taxonrank(self):
        return f"{self.taxon_kingdom} > {self.taxon_phylum} > {self.taxon_class} > {self.taxon_order} > {self.taxon_family} > {self.taxon_species}"

    def to_dict(self):
        return {
            "Source": self.source or "NA",
            "Source Key": self.id or "NA",
            "Status": self.taxonomic_status or "NA",
            "Rank": self.rank or "NA",
            "Accepted Name": self.accepted_name or "NA",
            "Scientific Name": self.scientific_name or "NA",
            "Canonical Name": self.canonical_name or "NA",
            "Authorship": self.authorship or "NA",
            "Kingdom": self.taxon_kingdom or "NA",
            "Phylum": self.taxon_phylum or "NA",
            "Class": self.taxon_class or "NA",
            "Order": self.taxon_order or "NA",
            "Family": self.taxon_family or "NA",
            "Genus": self.taxon_genus or "NA",
            "Species": self.taxon_species or "NA",
            "Threat Status": self.threat_status or "NA",
            "MatchType": self.match_type or "NA",
            "Confidence": self.match_confidence or "NA",
            "URL": self.url or "NA",
            "Search URL": self.search_url or "NA",
        }

    def __eq__(self, other):
        return self.source == other.source and self.id == other.id and self.scientific_name == other.scientific_name