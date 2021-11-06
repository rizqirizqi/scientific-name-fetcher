import os
import re
import requests
import sys
import getopt
import logging as log
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from helpers.string import fuzzy_search

# Load settings
load_dotenv()
INCLUDE_GBIF_SEARCH = os.getenv('INCLUDE_GBIF_SEARCH') == 'True'
AUTO_SEARCH_SIMILAR_SPECIES = os.getenv(
    'AUTO_SEARCH_SIMILAR_SPECIES') == 'True'

USAGE_HINT = 'Usage:\npipenv run python main.py -i <inputfile> -o <outputfile> -c <column> -v'

log.basicConfig(format='%(message)s', level=log.INFO)


# Functions
def list_get(l, idx, default = None):
  try:
    return l[idx]
  except IndexError:
    return default

def getRecommendedKeyword(query):
    log.debug(f'getRecommendedKeyword: {query}...')
    response = requests.get('https://commons.wikimedia.org/w/api.php?action=opensearch&search={}'.format(query))
    data = response.json()
    if list_get(data[1], 0):
        log.debug('found!')
        return list_get(data[1], 0)
    else:
        log.debug('notfound!')
        return 'Not Found'

def getDescription(query):
    log.debug(f'getDescription: {query}...')
    response = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=*&exintro=&explaintext=&generator=search&gsrsearch={}'.format(query))
    if response.status_code == 200:
        data = response.json()
        if data.get('query'):
            pages = data['query']['pages'].values()
            sorted_pages = sorted(list(pages), key=lambda item: item['index'])
            extracts = ''
            for p in sorted_pages:
                if fuzzy_search(p['extract'], query):
                    extracts += p['extract'] + '\n'
            log.debug('found!')
            return extracts.strip()
        else:
            log.debug('notfound!')
            return 'Not Found'
    else:
        log.debug('error!')
        return 'Error'


def getGBIFSearch(query):
    log.debug(f'getGBIFSearch: {query}...')
    response = requests.get(
        'http://api.gbif.org/v1/species/search?q={}&limit=6'.format(query))
    if response.status_code == 200:
        data = response.json()
        if data and data['count'] > 0:
            summary = 'GBIF SEARCH:\nResult: {}\n'.format(data['count'])
            for data in data['results']:
                summary += '{} {} | {} | {} | Taxonrank: {} > {} > {} > {} > {} > {} > {}\n'.format(
                    data.get('taxonomicStatus'),
                    data.get('rank'),
                    data.get('canonicalName'),
                    data.get('authorship'),
                    data.get('kingdom'),
                    data.get('phylum'),
                    data.get('class'),
                    data.get('order'),
                    data.get('family'),
                    data.get('genus'),
                    data.get('species'))
            log.debug('found!')
            return summary.strip()
        else:
            log.debug('notfound!')
            return 'Not Found'
    else:
        log.debug('error!')
        return 'Error'


def getScientificName(query):
    log.debug(f'getScientificName: {query}...')
    args = {
        'q': query,
        'language': 'en'
    }
    response = requests.get(
        'http://api.gbif.org/v1/species/search', params=args)
    if response.status_code == 200:
        data = response.json()
        for result in data['results']:
            species = result.get('species')
            if species:
                log.debug('found!')
                return species
    log.debug('notfound!')
    return query


def getGBIFMatch(query):
    log.debug(f'getGBIFMatch: {query}...')
    response = requests.get(
        'http://api.gbif.org/v1/species/match?name={}'.format(query))
    if response.status_code == 200:
        data = response.json()
        if data['matchType'] != 'NONE':
            if data.get('rank') != 'SPECIES':
                log.debug('notfound!')
                return getGBIFSearch(query)
            else:
                log.debug('found!')
                return 'GBIF MATCH: {} {} | {} {} | {} | {}\nTaxonrank: {} > {} > {} > {} > {} > {} > {}'.format(
                    data.get('matchType'),
                    data.get('confidence'),
                    data.get('status'),
                    data.get('rank'),
                    data.get('canonicalName'),
                    data.get('authorship'),
                    data.get('kingdom'),
                    data.get('phylum'),
                    data.get('class'),
                    data.get('order'),
                    data.get('family'),
                    data.get('genus'),
                    data.get('species'))
        elif INCLUDE_GBIF_SEARCH:
            return getGBIFSearch(query)
        else:
            log.debug('notfound!')
            return 'Not Found'
    else:
        log.debug('error!')
        return 'Error'


def readArgs():
    inputfile = 'input.txt'
    outputfile = datetime.now().strftime('result.%Y-%m-%d.%H%M%S.txt')
    column = 'Names'  # default column name to be read from csv files
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvi:o:c:', [
                                   'ifile=', 'ofile=', 'column='])
    except getopt.GetoptError:
        log.info(USAGE_HINT)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            log.info(USAGE_HINT)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
        elif opt in ('-c', '--column'):
            column = arg
        elif opt in ('-v', '--verbose'):
            log.getLogger().setLevel(level=log.DEBUG)
    log.info(f'Input file: {inputfile}')
    log.info(f'Output file: {outputfile}')
    log.info(f'Column: {column}')
    log.info('---------------------------------------------')
    return inputfile, outputfile, column


if __name__ == '__main__':
    # Setup File
    inputfile, outputfile, column = readArgs()
    if not os.path.isfile(inputfile):
        log.error("Input file not found, please check your command.")
        log.info(USAGE_HINT)
        sys.exit()

    # Read Input
    try:
        scientific_names = []
        if('.txt' in inputfile):
            with open(inputfile, 'r') as filehandle:
                scientific_names = [name.rstrip()
                                    for name in filehandle.readlines()]
        elif('.csv' in inputfile):
            scientific_names = pd.read_csv(inputfile)[column].tolist()
        elif('.xlsx' in inputfile):
            scientific_names = pd.read_excel(inputfile)[column].tolist()
    except KeyError:
        log.error('Error: The "{}" column does not exist on the input file'.format(column))
        log.error('Change the input file to contain the "{}" column'.format(column))
        log.error('or provide a custom column name with the "--column" arg')
        log.info(USAGE_HINT)
        exit(0)

    # Fetch and Write Output
    f = open(outputfile, 'a', encoding='utf8')
    log.info('Starting, it may take a while, please wait...')
    try:
        for name in scientific_names:
            log.info(f'## Looking up: {name}')
            
            # Non-scientific search tag enabled
            if name[-2:] == '-n':
                name = getScientificName(name[:-2])

            # Get Description
            description = getDescription(name)
            # Get Recommended Keyword
            if description == 'Not Found':
                reco_keyword = getRecommendedKeyword(name)
                if reco_keyword != 'Not Found':
                    description = 'Do you mean: {}'.format(reco_keyword)
            # Get GBIF Data from name
            gbif_data = getGBIFMatch(name)
            # Get GBIF Data from similar name
            if gbif_data == 'Not Found' and AUTO_SEARCH_SIMILAR_SPECIES and description != 'Not Found':
                similar_name = list_get(re.findall(name.split()[0] + ' [a-z]+', description), 0)
                if similar_name:
                    gbif_data = getGBIFMatch(similar_name)
            # Get GBIF Data from first word
            if gbif_data == 'Not Found' and name.split()[0] != name:
                gbif_data = getGBIFMatch(name.split()[0])
            f.write('### ' + name)
            f.write('\n')
            f.write(description or 'Not Found')
            f.write('\n')
            f.write(gbif_data or 'Not Found')
            f.write('\n')
            f.write('\n')
        log.info('Done! :D')
    except requests.exceptions.RequestException:
        log.error("There was problem connecting to the APIs, check your internet connection and try again")
    except Exception as e:
        log.exception("Exception occurred")
