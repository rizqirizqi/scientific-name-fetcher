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
   pipenv run python main.py -i input.txt
   ```
6. The result will be placed in a file named `result.*.txt`

### Help
```sh
pipenv run python main.py --help
```

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
