# Upbank Exporter

upbank exporter is a Python script to generate month-wise CSV files using the [Upbank API](https://developer.up.com.au/)

## Installation

```bash
python setup.py install
```

## Usage

You will need a file with the Up API Personal Access Token string inside to pass to the script. [Upbank Token](https://api.up.com.au/getting_started)
By default the script will check `./access_token` without needing to pass as argument.

```bash
usage: upbank-export [-h] [-year [year]] [-month [month]] [-token-file [file]]

Up Bank CSV Exporter.

options:
  -h, --help          show this help message and exit
  -year [year]
  -month [month]
  -token-file [file]
```

## Comments

I wrote this for my own personal usage. If you come across this and want it to do something else or are having problems please submit an issue.
