from re import sub

def threat_status_name_to_symbol(status):
    status = sub(r"[^\w]", " ", status).strip().replace("_", " ").upper()
    threat_status = {
        "NOT EVALUATED": "NE",
        "DATA DEFICIENT": "DD",
        "LEAST CONCERN": "LC",
        "NEAR THREATENED": "NT",
        "VULNERABLE": "VU",
        "ENDANGERED": "EN",
        "CRITICALLY ENDANGERED": "CR",
        "EXTINCT IN THE WILD": "EW",
        "EXTINCT": "EX",
    }
    return threat_status.get(status) or None


def threat_status_symbol_to_name(status):
    threat_status = {
        "NE": "NOT EVALUATED",
        "DD": "DATA DEFICIENT",
        "LC": "LEAST CONCERN",
        "NT": "NEAR THREATENED",
        "VU": "VULNERABLE",
        "EN": "ENDANGERED",
        "CR": "CRITICALLY ENDANGERED",
        "EW": "EXTINCT IN THE WILD",
        "EX": "EXTINCT",
    }
    return threat_status.get(status) or None
