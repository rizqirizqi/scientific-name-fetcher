import os
import requests
import sys
import getopt
import logging as log
from datetime import datetime
from pandas import read_csv, read_excel, DataFrame
from dotenv import load_dotenv
from scifetcher.config import ENV_CONFIG
from scifetcher.helpers.concurrent import run_concurrently
from scifetcher.models.search_result import SearchResult
from scifetcher.serializer import serialize
from scifetcher.services.gbif_service import GbifService
from scifetcher.services.iucn_service import IucnService
from scifetcher.services.wiki_service import WikiService

# Load settings
load_dotenv()

USAGE_HINT = "\
USAGE:\n\
pipenv run python -m scifetcher <OPTIONS>\n\
\n\
OPTIONS:\n\
    -s <source>                 | Set data source. Available source: GBIF, IUCN\n\
    -i <inputfile>              | Set input file\n\
    -o <outputfile>             | Set output file\n\
    --id-col <id_column>        | Set id column from input csv/xlsx\n\
    --name-col <name_column>    | Set name column from input csv/xlsx\n\
    -v                          | Verbose log\n\
\n\
EXAMPLES:\n\
    Normal usage:           pipenv run python -m scifetcher -i samples/input.csv -o output.csv\n\
    Set data source:        pipenv run python -m scifetcher -i samples/input.csv -o output.csv -s IUCN\n\
    Set id and name column: pipenv run python -m scifetcher -i samples/input.csv -o output.csv --id-col ID --name-col ScientificName\n\
    Verbose log:            pipenv run python -m scifetcher -i samples/input.csv -o output.csv -v\n\
    Show help message:      pipenv run python -m scifetcher -h\n\
"

log.basicConfig(format="%(message)s", level=log.INFO)


def read_args():
    inputfile = "input.txt"
    outputfile = datetime.now().strftime("result.%Y-%m-%d.%H%M%S.txt")
    source = "ALL"
    id_column = None
    name_column = "Names"  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvi:o:s:",
            ["ifile=", "ofile=", "source=", "id-col=", "name-col="],
        )
    except getopt.GetoptError:
        log.info(USAGE_HINT)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            log.info(USAGE_HINT)
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("--id-col"):
            id_column = arg
        elif opt in ("--name-col"):
            name_column = arg
        elif opt in ("-v", "--verbose"):
            log.getLogger().setLevel(level=log.DEBUG)
    log.info(f"Input file: {inputfile}")
    log.info(f"Output file: {outputfile}")
    if source != "ALL":
        log.info(f"Source: {source}")
    if id_column:
        log.info(f"ID Column: {id_column}")
    log.info(f"Name Column: {name_column}")
    log.info("---------------------------------------------")
    return inputfile, outputfile, source, name_column, id_column


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
        log.error(f'[Error] The "{column}" column does not exist on the input file')
        log.error(f"Change the input file to contain the correct column")
        log.error(
            'or provide a custom column name with the "--id-col" or "--name-col" arg'
        )
        log.info(USAGE_HINT)
        sys.exit(2)


if __name__ == "__main__":
    # Read args and setup File
    inputfile, outputfile, source, name_column, id_column = read_args()
    if not os.path.isfile(inputfile):
        log.error("Input file not found, please check your command.")
        log.info(USAGE_HINT)
        sys.exit(2)

    # Show warnings and errors
    if source == "IUCN" and not ENV_CONFIG["IUCN_API_TOKEN"]:
        log.error(
            "[Error] IUCN_API_TOKEN is not set, set it on .env file if you need data source from IUCN"
        )
        sys.exit(2)
    elif not ENV_CONFIG["IUCN_API_TOKEN"]:
        log.warning(
            "[Warning] IUCN_API_TOKEN is not set, set it on .env file if you need data source from IUCN"
        )

    # Read Input
    scientific_names = read_input(inputfile, name_column, id_column)

    # Fetch and Write Output
    log.info("Starting, it may take a while, please wait...")
    search_result_list = []
    try:
        # Fetch Species
        for index, row in scientific_names.iterrows():
            key = row[id_column] if id_column else index
            name = row[name_column]
            log.info(f"## Looking up: {name}")

            # Non-scientific search tag enabled
            if name[-2:] == "-n":
                name = GbifService().fetch_scientific_name(name[:-2])

            search_result = SearchResult(key, name)
            # Get Wiki Result
            description = WikiService().fetch_data(name)
            search_result.set_description(description)
            # Get Species Result
            [gbif_species_list, iucn_species_list] = run_concurrently(
                [
                    (GbifService().fetch_data, (name, description))
                    if source in ["ALL", "GBIF"]
                    else None,
                    (IucnService().fetch_data, (name, description))
                    if source in ["ALL", "IUCN"] and ENV_CONFIG["IUCN_API_TOKEN"]
                    else None,
                ]
            )
            if gbif_species_list:
                search_result.extend(gbif_species_list)
            if iucn_species_list:
                search_result.extend(iucn_species_list)

            search_result_list.append(search_result)

        log.info("Done! :D")
    except Exception as e:
        log.exception(
            "[Error] Error occurred. Please try again. Contact the maintainer if the problem persist."
        )

    # Write Output
    try:
        serialize(outputfile, search_result_list)
    except Exception as e:
        log.exception(
            "[Error] Can't write output. Please try again. Contact the maintainer if the problem persist."
        )
