# scientific-name-fetcher (scifetcher)

[![contributions welcome][contrib-badge]][contrib-url]
[![MIT License][license-badge]][license-url]

[![Watch on GitHub][github-watch-badge]][github-watch]
[![Star on GitHub][github-star-badge]][github-star]
[![Tweet][twitter-badge]][twitter]

Fetch plants/animals scientific name information from the internet.

Current supported sources:
- [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki). See [Docs](https://www.mediawiki.org/wiki/API:Main_page).
- [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/). See [Docs](https://www.gbif.org/developer).
- [International Union for Conservation of Nature (IUCN)](https://apiv3.iucnredlist.org/). See [Docs](https://apiv3.iucnredlist.org/api/v3/docs). ([Need API Token](#available-settings))
- [Plants of the World Online (POWO)](https://powo.science.kew.org/). See [Docs](https://github.com/RBGKew/pykew).

## Requirements
- [python >= 3.7](https://www.python.org/downloads/) (you can use [pyenv](https://github.com/pyenv/pyenv) for easier python version management)
- [pipenv](https://pipenv.pypa.io/en/latest/)

<details>
   <summary>Detailed Guide for Windows</summary>

   1. Download python from https://www.python.org/downloads/
   2. Install python, follow the instruction
   3. Press Win button (something like window icon on keyboard), search "env", then open `Edit the system environment variables`
   4. Click Environment Variables
   5. On `System Variables` section, edit the `Path` key
   6. Add these paths using the `New` button:
      ```
      # Please replace the username with your windows username, you can see it in C:\Users folder
      # Please replace the python version with your installed python version
      C:\Users\<YOUR_USERNAME>\AppData\Local\Programs\Python\Python310
      C:\Users\<YOUR_USERNAME>\AppData\Local\Programs\Python\Python310\Scripts
      C:\Users\<YOUR_USERNAME>\AppData\Roaming\Python\Python310\Scripts
      ```
   7. Click OK, then OK
   8. Open cmd, then type `python --version`, then it should respond with the python version.
   9. Type `pip3 install --user pipenv`, then it should install pipenv, make sure it's successfully installed.
   10. Type `pipenv --version`, then it should respond with the pipenv version.
   11. Done! You can continue follow the guide in the "How to run" section.
</details>


## How to run
1. Clone
   ```sh
   git clone git@github.com:rizqirizqi/scientific-name-fetcher.git
   cd scientific-name-fetcher
   ```
2. Copy env
 
   Linux:
   ```sh
   cp env.sample .env
   ```
   Windows:
   ```sh
   copy env.sample .env
   ```
3. Install dependencies
   ```sh
   pipenv --python 3
   pipenv install
   ```
4. Fill your input in `input.txt`, please look at `samples/input.txt` for example. You can also use csv or xlsx if you want.
5. Run
   ```sh
   pipenv run python -m scifetcher -i input.txt
   ```
6. The result will be placed in a file named `result.*.txt`

### Help
```sh
pipenv run python -m scifetcher --help
```

## Settings

1. Edit .env file (see env.sample file for reference)
2. Change the settings

### Available settings:

| Setting                     | Default | Description |
|-----------------------------|:-------:|-------------|
| AUTO_SEARCH_SIMILAR_SPECIES |  True   | Search GBIF database with similar name from wikipedia result. |
| INCLUDE_GBIF_SEARCH         |  True   | Include GBIF search result if it can't find the exact match of the scientific name. |
| IUCN_API_TOKEN              |    -    | Required token to fetch data from IUCN API. Request a token [here](https://apiv3.iucnredlist.org/api/v3/token). |

## Contributing
1. Fork this repo
2. Develop
3. Create pull request
4. Tag [@rizqirizqi](https://github.com/rizqirizqi) for review
5. Merge~~

### Run Test
```
# all
pipenv run python -m unittest
# one file
pipenv run python -m unittest tests
# coverage
pipenv run coverage run -m unittest
coverage report
coverage html && xdg-open ./htmlcov/index.html
```

### Lint
If you're using VSCode:
1. Open the Command Palette in the `View` menu (or just Ctrl+Shift+P)
2. Type `Python: Select Interpreter`
3. Select `scientific-name-fetcher`
4. Choose `pipenv`

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
