# scientific-name-fetcher

[![contributions welcome][contrib-badge]][contrib-url]
[![MIT License][license-badge]][license-url]

[![Watch on GitHub][github-watch-badge]][github-watch]
[![Star on GitHub][github-star-badge]][github-star]
[![Tweet][twitter-badge]][twitter]

Fetch plants/animals scientific name information from the internet

Current supported sources:
- Wikipedia
- Global Biodiversity Information Facility (GBIF)

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

## Contributing
1. Fork this repo
2. Develop
3. Create pull request
4. Tag [@rizqirizqi](https://github.com/rizqirizqi) for review
5. Merge~~

## License

MIT

[contrib-badge]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square
[contrib-url]: https://github.com/rizqirizqi/scientific-name-fetcher/issues
[license-badge]: https://img.shields.io/npm/l/webpconvert.svg?style=flat-square
[license-url]: https://github.com/rizqirizqi/webpconvert/blob/master/LICENSE

[github-watch-badge]: https://img.shields.io/github/watchers/rizqirizqi/scientific-name-fetcher.svg?style=social
[github-watch]: https://github.com/rizqirizqi/scientific-name-fetcher/watchers
[github-star-badge]: https://img.shields.io/github/stars/rizqirizqi/scientific-name-fetcher.svg?style=social
[github-star]: https://github.com/rizqirizqi/scientific-name-fetcher/stargazers
[twitter]: https://twitter.com/intent/tweet?text=Check%20out%20this%20CLI%20converter%20from%20png%2Fjpg%20images%20to%20webp!%20https%3A%2F%2Fgithub.com%2Frizqirizqi%2Fscientific-name-fetcher
[twitter-badge]: https://img.shields.io/twitter/url/https/github.com/rizqirizqi/scientific-name-fetcher.svg?style=social