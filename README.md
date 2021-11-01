# scientific-name-fetcher

[![contributions welcome][contrib-badge]][contrib-url]
[![MIT License][license-badge]][license-url]

[![Watch on GitHub][github-watch-badge]][github-watch]
[![Star on GitHub][github-star-badge]][github-star]
[![Tweet][twitter-badge]][twitter]

Fetch plants/animals scientific name information from the internet.

Current supported sources:
- Wikipedia
- Global Biodiversity Information Facility (GBIF)

## Requirements
- [python >= 3.7](https://www.python.org/downloads/) (you can use [pyenv](https://github.com/pyenv/pyenv) for easier python version management)
- [pipenv](https://pipenv.pypa.io/en/latest/)

## How to run
1. Install dependencies
   ```python
   cp env.sample .env
   pipenv --python 3
   pipenv install
   ```
2. Fill your input in `input.txt`, please look at `samples/input.txt` for example. You can also use csv or xlsx if you want.
3. Run
   ```
   pipenv run python main.py
   # or
   pipenv run python main.py -i path/to/input-file.txt -o path/to/output-file.txt
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

GPL-3.0

[contrib-badge]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square
[contrib-url]: https://github.com/rizqirizqi/scientific-name-fetcher/issues
[license-badge]: https://img.shields.io/npm/l/webpconvert.svg?style=flat-square
[license-url]: https://github.com/rizqirizqi/webpconvert/blob/master/LICENSE

[github-watch-badge]: https://img.shields.io/github/watchers/rizqirizqi/scientific-name-fetcher.svg?style=social
[github-watch]: https://github.com/rizqirizqi/scientific-name-fetcher/watchers
[github-star-badge]: https://img.shields.io/github/stars/rizqirizqi/scientific-name-fetcher.svg?style=social
[github-star]: https://github.com/rizqirizqi/scientific-name-fetcher/stargazers
[twitter]: https://twitter.com/intent/tweet?text=Fetch%20plants%20and%20animals%20scientific%20name%20information%20from%20the%20internet!%20https%3A%2F%2Fgithub.com%2Frizqirizqi%2Fscientific-name-fetcher
[twitter-badge]: https://img.shields.io/twitter/url/https/github.com/rizqirizqi/scientific-name-fetcher.svg?style=social
