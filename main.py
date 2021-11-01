import os
import re
import requests
import sys, getopt
from datetime import datetime
from distutils.util import strtobool
import pandas as pd
from logger import Logger 

from dotenv import load_dotenv

logger = Logger()

# Load settings
load_dotenv()
INCLUDE_GBIF_SEARCH = strtobool(os.getenv('INCLUDE_GBIF_SEARCH'))
AUTO_SEARCH_SIMILAR_SPECIES = strtobool(os.getenv('AUTO_SEARCH_SIMILAR_SPECIES'))

# Functions
def getDescription(query):
  response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=*&exintro=&explaintext=&generator=search&gsrsearch={}'.format(query))
  if response.status_code == 200:
    data = response.json()
    if data.get('query'):
      pages = data['query']['pages'].values()
      sorted_pages = sorted(list(pages), key=lambda item: item['index'])
      extracts = ''
      for p in sorted_pages:
        if query.split()[0] in p['extract']:
          extracts += p['extract'] + '\n'
      return extracts.strip()
    else:
      return 'Not Found'
  else:
    return 'Error'

def getGBIFSearch(query):
  response = requests.get('http://api.gbif.org/v1/species/search?q={}&limit=6'.format(query))
  if response.status_code == 200:
    data = response.json()
    if data and data['count'] > 0:
      summary = 'GBIF SEARCH:\nResult: {}\n'.format(data['count'])
      for data in data['results']:
        summary += '{} {} | {} | {} | Taxonrank: {} > {} > {} > {} > {}\n'.format(data.get('taxonomicStatus'), data.get('rank'), data.get('canonicalName'), data.get('authorship'), data.get('kingdom'), data.get('phylum'), data.get('class'), data.get('order'), data.get('family'))
      return summary.strip()
    else:
      return 'Not Found'
  else:
    return 'Error'

def getScientificName(query):
    args = {
      'q': query,
      'language': 'en'
    }
    response = requests.get('http://api.gbif.org/v1/species/search', params=args)
    if response.status_code == 200:
      data = response.json()
      for result in data['results']:
        species = result.get('species')
        if species:
          return species
    return query

def getGBIFData(query):
  response = requests.get('http://api.gbif.org/v1/species/match?name={}'.format(query))
  if response.status_code == 200:
    data = response.json()
    if data['matchType'] != 'NONE':
      return 'GBIF MATCH: {} {} | {} {} | {} | {}'.format(data.get('matchType'), data.get('confidence'), data.get('status'), data.get('rank'), data.get('canonicalName'), data.get('authorship'))
    elif INCLUDE_GBIF_SEARCH:
      return getGBIFSearch(query)
    else:
      return 'Not Found'
  else:
    return 'Error'

def readArgs():
  inputfile = 'input.txt'
  outputfile = datetime.now().strftime('result.%Y-%m-%d.%H:%M:%S.txt')
  usage_hint = 'python main.py -i <inputfile> -o <outputfile>'
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['ifile=','ofile='])
  except getopt.GetoptError:
    print(usage_hint)
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(usage_hint)
        sys.exit()
    elif opt in ('-i', '--ifile'):
        inputfile = arg
    elif opt in ('-o', '--ofile'):
        outputfile = arg
  # print(bcolors.OKGREEN + 'Input file:', inputfile)
  logger.success(f"Input file: {inputfile}")
  logger.success(f"Output file: {outputfile}")
  return inputfile, outputfile

if __name__ == '__main__':
  try:
    # Setup File
    inputfile, outputfile = readArgs()

    # Read Input
    scientific_names = []
    if('.txt' in inputfile):
      with open(inputfile, 'r') as filehandle:
        scientific_names = [name.rstrip() for name in filehandle.readlines()]
    elif('.csv' in inputfile):
      scientific_names = pd.read_csv(inputfile)['Names'].tolist()
    elif('.xlsx' in inputfile):
      scientific_names = pd.read_excel(inputfile)['Names'].tolist()


    # Fetch and Write Output
    f = open(outputfile, 'a')
    logger.warn('Starting, it may take a while, please wait...')
    for name in scientific_names:
      # Non-scientific search tag enabled
      if name[-2:] == '-n':
        name = getScientificName(name[:-2])
        
      logger.info(f"Looking up: {name}")

      # Get Description
      description = getDescription(name)
      # Get GBIF Data from name
      gbif_data = getGBIFData(name)
      # Get GBIF Data from similar name
      if gbif_data == 'Not Found' and AUTO_SEARCH_SIMILAR_SPECIES and description != 'Not Found':
        similar_name = re.search(name.split()[0] + ' .+', description)
        gbif_data = getGBIFData(similar_name)
      # Get GBIF Data from first word
      if gbif_data == 'Not Found' and name.split()[0] != name:
        gbif_data = getGBIFData(name.split()[0])
      f.write('### ' + name)
      f.write('\n')
      f.write(description or 'Not Found')
      f.write('\n')
      f.write(gbif_data or 'Not Found')
      f.write('\n')
      f.write('\n')
    logger.success("\nDone! :D")
  except KeyboardInterrupt:
    logger.error("Exiting...")