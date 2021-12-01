from pandas import DataFrame, concat


def serialize(outputfile, search_result_list):
    if ".txt" in outputfile:
        serialize_txt(outputfile, search_result_list)
    elif ".csv" in outputfile:
        serialize_csv(outputfile, search_result_list)
    elif ".xlsx" in outputfile:
        serialize_excel(outputfile, search_result_list)


def serialize_txt(outputfile, search_result_list):
    f = open(outputfile, "a", encoding="utf8")
    for search_result in search_result_list:
        f.write("### " + search_result.query)
        f.write("\n")
        f.write(search_result.description or "Not Found")
        f.write("\n")
        for species in search_result.species_list:
            if species.match_type.lower() == "exact":
                f.write(
                    "{} MATCH: {} {} | {} {} | {} | {} | {}\nTaxonrank: {}".format(
                        species.source,
                        species.match_type,
                        species.match_confidence,
                        species.taxonomic_status,
                        species.rank,
                        species.accepted_name,
                        species.canonical_name,
                        species.authorship,
                        species.get_taxonrank(),
                    )
                )
            else:
                f.write(
                    "{} SEARCH: {} {} | {} | {} | {} | Taxonrank: {}".format(
                        species.source,
                        species.taxonomic_status,
                        species.rank,
                        species.accepted_name,
                        species.canonical_name,
                        species.authorship,
                        species.get_taxonrank(),
                    )
                )
            f.write("\n")
        f.write("\n")


def serialize_csv(outputfile, search_result_list):
    df = generate_dataframe(search_result_list)
    df.to_csv(outputfile, encoding="utf-8-sig")


def serialize_excel(outputfile, search_result_list):
    df = generate_dataframe(search_result_list)
    df.to_excel(outputfile)


def generate_dataframe(search_result_list):
    frames = []
    for search_result in search_result_list:
        if len(search_result.species_list) <= 0: continue
        spec_list = DataFrame.from_records(
            [
                {**{"Key": search_result.key, "Verbatim": search_result.query}, **s.to_dict()}
                for s in search_result.species_list
            ],
            index="Key"
        )
        frames.append(spec_list)
    if len(frames) <= 0: return DataFrame(frames)
    return concat(frames)
