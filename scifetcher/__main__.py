import os
import re
import requests
import sys
import getopt
import logging as log
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from scifetcher.apiclients.gbif_api import GbifApi
from scifetcher.apiclients.wiki_api import WikiApi
from scifetcher.helpers.list import list_get

# Load settings
load_dotenv()
AUTO_SEARCH_SIMILAR_SPECIES = os.getenv("AUTO_SEARCH_SIMILAR_SPECIES") == "True"

USAGE_HINT = "Usage:\npipenv run python -m scifetcher -i <inputfile> -o <outputfile> -c <column> -v"

log.basicConfig(format="%(message)s", level=log.INFO)


def readArgs():
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
            sys.exit()
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


if __name__ == "__main__":
    # Setup File
    inputfile, outputfile, column = readArgs()
    if not os.path.isfile(inputfile):
        log.error("Input file not found, please check your command.")
        log.info(USAGE_HINT)
        sys.exit()

    # Read Input
    try:
        scientific_names = []
        if ".txt" in inputfile:
            with open(inputfile, "r") as filehandle:
                scientific_names = [name.rstrip() for name in filehandle.readlines()]
        elif ".csv" in inputfile:
            scientific_names = pd.read_csv(inputfile)[column].tolist()
        elif ".xlsx" in inputfile:
            scientific_names = pd.read_excel(inputfile)[column].tolist()
    except KeyError:
        log.error(
            'Error: The "{}" column does not exist on the input file'.format(column)
        )
        log.error('Change the input file to contain the "{}" column'.format(column))
        log.error('or provide a custom column name with the "--column" arg')
        log.info(USAGE_HINT)
        exit(0)

    # Fetch and Write Output
    f = open(outputfile, "a", encoding="utf8")
    log.info("Starting, it may take a while, please wait...")
    try:
        for name in scientific_names:
            log.info(f"## Looking up: {name}")

            # Non-scientific search tag enabled
            if name[-2:] == "-n":
                name = GbifApi(name[:-2]).get_scientific_name()

            # Get Description
            wiki_result = WikiApi(name)
            description = wiki_result.get_description()
            # Get Recommended Keyword
            if description == "Not Found":
                reco_keyword = wiki_result.get_recommended_keyword()
                if reco_keyword != "Not Found":
                    description = "Do you mean: {}".format(reco_keyword)
            # Get GBIF Data from name
            gbif_data = GbifApi(name).get_gbif_match()
            # Get GBIF Data from similar name
            if (
                gbif_data == "Not Found"
                and AUTO_SEARCH_SIMILAR_SPECIES
                and description != "Not Found"
            ):
                similar_name = list_get(
                    re.findall(name.split()[0] + " [a-z]+", description), 0
                )
                if similar_name:
                    gbif_data = GbifApi(similar_name).get_gbif_match()
            # Get GBIF Data from first word
            if gbif_data == "Not Found" and name.split()[0] != name:
                gbif_data = GbifApi(name.split()[0]).get_gbif_match()
            f.write("### " + name)
            f.write("\n")
            f.write(description or "Not Found")
            f.write("\n")
            f.write(gbif_data or "Not Found")
            f.write("\n")
            f.write("\n")
        log.info("Done! :D")
    except requests.exceptions.RequestException:
        log.error(
            "There was problem connecting to the APIs, check your internet connection and try again"
        )
    except Exception as e:
        log.exception("Exception occurred")
