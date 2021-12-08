import os
import requests
import sys
import getopt
import logging as log
from datetime import datetime
from pandas import read_csv, read_excel, DataFrame
from dotenv import load_dotenv
from scifetcher.helpers.concurrent import run_concurrently
from scifetcher.models.search_result import SearchResult
from scifetcher.serializer import serialize
from scifetcher.services.gbif_service import GbifService
from scifetcher.services.iucn_service import IucnService
from scifetcher.services.wiki_service import WikiService
from scifetcher.models.species import Species

# Load settings
load_dotenv()

USAGE_HINT = "USAGE:\npipenv run python -m scifetcher <OPTIONS>\n\nOPTIONS:\n-i <inputfile>\n-o <outputfile>\n--id-col <id_column>\n--name-col <name_column>\n-v"

log.basicConfig(format="%(message)s", level=log.INFO)


def read_args():
    inputfile = "input.txt"
    outputfile = datetime.now().strftime("result.%Y-%m-%d.%H%M%S.txt")
    id_column = None
    name_column = "Names"  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvi:o:c:", ["ifile=", "ofile=", "id-col=", "name-col="]
        )
    except getopt.GetoptError:
        log.info(USAGE_HINT)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            log.info(USAGE_HINT)
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("--id-col"):
            id_column = arg
        elif opt in ("--name-col"):
            name_column = arg
        elif opt in ("-v", "--verbose"):
            log.getLogger().setLevel(level=log.DEBUG)
    log.info(f"Input file: {inputfile}")
    log.info(f"Output file: {outputfile}")
    if id_column:
        log.info(f"ID Column: {id_column}")
    log.info(f"Name Column: {name_column}")
    log.info("---------------------------------------------")
    return inputfile, outputfile, name_column, id_column


def read_input(inputfile, name_column, id_column) -> DataFrame:
    try:
        scientific_names = []
        if ".txt" in inputfile:
            with open(inputfile, "r") as filehandle:
                scientific_names = DataFrame(
                    {name_column: [name.rstrip() for name in filehandle.readlines()]}
                )
        elif ".csv" in inputfile:
            scientific_names = read_csv(inputfile)
            if id_column and not id_column in scientific_names:
                raise KeyError(id_column)
            if not name_column in scientific_names:
                raise KeyError(name_column)
        elif ".xlsx" in inputfile:
            scientific_names = read_excel(inputfile)
            if id_column and not id_column in scientific_names:
                raise KeyError
            if not name_column in scientific_names:
                raise KeyError
        return scientific_names
    except KeyError as column:
        log.error(f'Error: The "{column}" column does not exist on the input file')
        log.error(f"Change the input file to contain the correct column")
        log.error(
            'or provide a custom column name with the "--id-col" or "--name-col" arg'
        )
        log.info(USAGE_HINT)
        sys.exit(2)


if __name__ == "__main__":
    # Setup File
    inputfile, outputfile, name_column, id_column = read_args()
    if not os.path.isfile(inputfile):
        log.error("Input file not found, please check your command.")
        log.info(USAGE_HINT)
        sys.exit(2)

    # Read Input
    scientific_names = read_input(inputfile, name_column, id_column)

    # Fetch and Write Output
    log.info("Starting, it may take a while, please wait...")
    try:
        # Fetch Species
        search_result_list = []
        for index, row in scientific_names.iterrows():
            key = row[id_column] if id_column else index
            name = row[name_column]
            log.info(f"## Looking up: {name}")

            # Non-scientific search tag enabled
            if name[-2:] == "-n":
                gbif_service = GbifService()
                name = gbif_service.fetch_scientific_name(name[:-2])

            search_result = SearchResult(key, name)
            # Get Wiki Result
            wiki_service = WikiService()
            description = wiki_service.fetch_data(name)
            search_result.set_description(description)
            # Get Species Result
            gbif_service = GbifService()
            iucn_service = IucnService()
            [gbif_species_list, iucn_species_list] = run_concurrently(
                [
                    (gbif_service.fetch_data, (name, description)),
                    (iucn_service.fetch_data, (name, description)),
                ]
            )
            if gbif_species_list:
                search_result.extend(gbif_species_list)
            if iucn_species_list:
                search_result.extend(iucn_species_list)

            search_result_list.append(search_result)

        # Write Output
        serialize(outputfile, search_result_list)

        log.info("Done! :D")
    except Exception as e:
        log.exception(
            "Error occurred. Please try again. Contact the maintainer if the problem persist."
        )
