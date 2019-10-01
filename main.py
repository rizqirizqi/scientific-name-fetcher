import os
import requests
import json
import re
import datetime
from distutils.util import strtobool

from dotenv import load_dotenv

# Load settings
load_dotenv()
WITH_GBIF_SEARCH = strtobool(os.getenv('WITH_GBIF_SEARCH'))
AUTO_SEARCH_PREDICTED_SPECIES = strtobool(os.getenv('AUTO_SEARCH_PREDICTED_SPECIES'))

# Functions
def getDescription(query):
  response = requests.get('https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={}'.format(query))
  if response.status_code == 200:
    data = response.json()
    if len(data[2]) > 0:
      return data[2][0]
    else:
      return 'Not Found'
  else:
    return 'Error'

def getGBIFSearch(query):
  response = requests.get('http://api.gbif.org/v1/species/search?q={}&limit=6'.format(query))
  if response.status_code == 200:
    data = response.json()
    if data:
      return data
    else:
      return 'Not Found'
  else:
    return 'Error'

def getGBIFData(query):
  response = requests.get('http://api.gbif.org/v1/species/match?name={}'.format(query))
  if response.status_code == 200:
    data = response.json()
    if data['matchType'] != 'NONE':
      return 'GBIF MATCH: {} {} | {} {} | {} | {}'.format(data.get('matchType'), data.get('confidence'), data.get('status'), data.get('rank'), data.get('canonicalName'), data.get('authorship'))
    elif WITH_GBIF_SEARCH:
      search_result = getGBIFSearch(query)
      if search_result['count'] > 0:
        summary = 'GBIF SEARCH:\nResult: {}\n'.format(search_result['count'])
        for data in search_result['results']:
          try:
            summary += '{} {} | {} | {} | Taxonrank: {} > {} > {} > {} > {}\n'.format(data.get('taxonomicStatus'), data.get('rank'), data.get('canonicalName'), data.get('authorship'), data.get('kingdom'), data.get('phylum'), data.get('class'), data.get('order'), data.get('family'))
          except KeyError:
            summary += json.dumps(data)
        return summary
      else:
        return 'Not Found'
    else:
      return 'Not Found'
  else:
    return 'Error'

# Read Input
scientific_names = []
with open('input.txt', 'r') as filehandle:
    scientific_names = [name.rstrip() for name in filehandle.readlines()]

# Fetch and Write Output
now = datetime.datetime.now()
result_filename = now.strftime("result.%Y-%m-%d.%H:%M:%S.txt")
f = open(result_filename, "a")
print('Dancing...')
for name in scientific_names:
  print(name)
  description = getDescription(name.split()[0])
  gbif_query = name
  if AUTO_SEARCH_PREDICTED_SPECIES and description == 'Not Found':
    gbif_query = re.search('[A-Z][a-z]+', description)
  gbif_data = getGBIFData(gbif_query)
  if gbif_data == 'Not Found' and name.split()[0] != name:
    gbif_data = getGBIFData(name.split()[0])
  f.write(name)
  f.write('\n')
  f.write(description or 'Not Found')
  f.write('\n')
  f.write(gbif_data or 'Not Found')
  f.write('\n')
  f.write('\n')
