import os
import requests
import sys
import getopt
import logging as log
from datetime import datetime
from pandas import read_csv, read_excel
from dotenv import load_dotenv
from scifetcher.models.search_result import SearchResult
from scifetcher.serializer import serialize
from scifetcher.services.gbif_service import GbifService
from scifetcher.services.wiki_service import WikiService
from scifetcher.models.species import Species

# Load settings
load_dotenv()

USAGE_HINT = "Usage:\npipenv run python -m scifetcher -i <inputfile> -o <outputfile> -c <column> -v"

log.basicConfig(format="%(message)s", level=log.INFO)


def read_args():
    inputfile = "input.txt"
    outputfile = datetime.now().strftime("result.%Y-%m-%d.%H%M%S.txt")
    column = "Names"  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvi:o:c:", ["ifile=", "ofile=", "column="]
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
        elif opt in ("-c", "--column"):
            column = arg
        elif opt in ("-v", "--verbose"):
            log.getLogger().setLevel(level=log.DEBUG)
    log.info(f"Input file: {inputfile}")
    log.info(f"Output file: {outputfile}")
    log.info(f"Column: {column}")
    log.info("---------------------------------------------")
    return inputfile, outputfile, column


def read_input(inputfile):
    try:
        scientific_names = []
        if ".txt" in inputfile:
            with open(inputfile, "r") as filehandle:
                scientific_names = [name.rstrip() for name in filehandle.readlines()]
        elif ".csv" in inputfile:
            scientific_names = read_csv(inputfile)[column].tolist()
        elif ".xlsx" in inputfile:
            scientific_names = read_excel(inputfile)[column].tolist()
        return scientific_names
    except KeyError:
        log.error(f'Error: The "{column}" column does not exist on the input file')
        log.error(f'Change the input file to contain the "{column}" column')
        log.error('or provide a custom column name with the "--column" arg')
        log.info(USAGE_HINT)
        sys.exit(2)


if __name__ == "__main__":
    # Setup File
    inputfile, outputfile, column = read_args()
    if not os.path.isfile(inputfile):
        log.error("Input file not found, please check your command.")
        log.info(USAGE_HINT)
        sys.exit(2)

    # Read Input
    scientific_names = read_input(inputfile)

    # Fetch and Write Output
    log.info("Starting, it may take a while, please wait...")
    try:
        # Fetch Species
        search_result_list = []
        for name in scientific_names:
            log.info(f"## Looking up: {name}")

            # Non-scientific search tag enabled
            if name[-2:] == "-n":
                gbif_service = GbifService()
                name = gbif_service.fetch_scientific_name(name[:-2])

            search_result = SearchResult(name)
            # Get Wiki Result
            wiki_service = WikiService()
            description = wiki_service.fetch_data(name)
            search_result.set_description(description)
            # Get GBIF Result
            gbif_service = GbifService()
            gbif_species_list = gbif_service.fetch_data(name, description)
            search_result.extend(gbif_species_list)

            search_result_list.append(search_result)

        # Write Output
        serialize(outputfile, search_result_list)

        log.info("Done! :D")
    except Exception as e:
        log.exception(
            "Error occurred. Please try again. Contact the maintainer if the problem persist."
        )
