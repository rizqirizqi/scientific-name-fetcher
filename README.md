# scientific-name-fetcher

Fetch vegetations/animals scientific name information from the internet

Current supported sources:
- Wikipedia
- Global Biodiversity Information Facility

## Requirements
- [python >= 3.5](https://www.python.org/downloads/)
- [pipenv](https://pipenv.pypa.io/en/latest/)

## How to run
1. Install dependencies
   ```python
   cp env.sample .env
   pipenv --python 3
   pipenv install
   ```
2. Fill the input in `input.txt`, please look at `input.txt.sample`
3. Run
   ```
   pipenv run python3 main.py
   # or
   pipenv run python3 main.py -i path/to/input-file.txt -o path/to/output-file.txt
   ```
4. The result will be placed in a file named `result.*.txt`

## Settings

1. Edit .env file
2. Change the settings

### Available settings:

| Setting                     | Default | Description |
|-----------------------------|:-------:|------------:|
| INCLUDE_GBIF_SEARCH         |  True   | Include GBIF search result if it can't find the exact match of the scientific name |
| AUTO_SEARCH_SIMILAR_SPECIES |  True   | Search GBIF database with similar name from wikipedia result |
