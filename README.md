# Singer Tap - US Federal Reserve API

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)

## Overview

What is FRED? Short for Federal Reserve Economic Data, FRED is
an online database consisting of hundred of thousands of economic
data time series from scores of national, international, public, and
private sources. FRED, created and maintained by the Research Department at
the Federal Reserve Bank of St. Louis, goes far beyond simply providing data:
It combines data with a powerful mix of tools that help the user understand, interact
with, display, and disseminate the data. In essence, FRED helps users tell their
data stories. The purpose of this article is to guide the potential (or current)
FRED user through the various aspects and tools of the database.

## Setup

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

## Usage

### Step 1 - Install in Virtual Environment

We recommend using a virtualenv.

```terminal
> py -m venv venv/tap-federal-reserve
> venv/tap-federal-reserve/Scripts/activate
> pip install -e .
```

### Step 2 - Specify Configuration Values

In the `config.json` file you will need to provide a few things in order to get the Tap running.
Some of the values are required while some are optional. The both the required and optional arguments
are the following:

```jsonc
{
  // REQUIRED: Should be used on first sync to indicate how far back to grab records.
  "start_date": "2021-06-20",

  // REQUIRED: Your Federal Reserve API Key.
  "api_key": "<FRED_API_KEY>",

  // REQUIRED: The Series Id you want to pull. For example, `BOPGN`.
  "series_id": "BOPGN",

  // OPTIONAL: The starting period you want to pull data. Make sure
  // it's an ISO-Format Date.
  "series_start_date": "2020-12-31",

  // OPTIONAL: The end period you want to pull data. Make sure
  // it's an ISO-Format Date.
  "series_end_date": "2021-01-21"
}
```

### Step 3 - Run the Script

**Discovery Mode:**

To run the script, in discovery mode, open up your terminal and run the following command
after activating your virtual environment:

```terminal
tap-federal-reserve --config sample.config.json --discover
```

**Sync Mode:**

To run the script, in sync mode, open up your terminal and run the following command
after activating your virtual environment:

```terminal
tap-federal-reserve --config sample.config.json
```

<!--
```terminal
py venv/tap-us-federal-reserve/Scripts/tap-federal-reserve-script.py --config config.json
```

tap-federal-reserve --config config.json
py .venvs/tap-us-federal-reserve/Scripts/tap-federal-reserve-script.py --config config.json | .venvs/target-csv/Scripts/target-csv --config config.json -->
