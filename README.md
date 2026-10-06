# Web Scraping ETL Assignment

## Overview

This project implements a Python web scraping and data-processing pipeline using two public practice websites:

* Books to Scrape: https://books.toscrape.com/
* Quotes to Scrape: https://quotes.toscrape.com/

The pipeline performs:

1. Scraping
2. Cleaning
3. Validation
4. Deduplication
5. Consolidation
6. Output generation

The implementation follows pagination links dynamically and includes retry handling, logging, validation, duplicate detection, and automated tests.

---

## Python Version

The project was tested successfully with:

* Python 3.13.1

The assignment recommends Python 3.10–3.12. Python 3.13.1 was used for development and testing in the local environment.

---

## Project Structure

```text
project/
├── AI_USAGE.md
├── main.py
├── README.md
├── requirements.txt
├── logs/
│   └── scraper.log
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
└── tests/
    ├── test_cleaning.py
    ├── test_validation.py
    └── test_deduplication.py
```

---

## Installation and Setup

Create and activate a Python virtual environment if required.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Dependencies

The project uses:

* `requests` - HTTP requests
* `beautifulsoup4` - HTML parsing
* `lxml` - HTML parser
* `pytest` - automated testing

Dependencies are listed in `requirements.txt`.

---

## How to Run

Run the complete scraping pipeline from the project root:

```bash
python main.py
```

The program scrapes both sources, processes the records, writes the final dataset and summary report, and records execution details in the log file.

---

## Pagination

Pagination is handled dynamically for both websites.

The scrapers:

1. Process the current page.
2. Find the `Next` pagination link.
3. Resolve the next URL using `urljoin`.
4. Continue until a `Next` link is no longer available.

Page numbers are not hard-coded.

---

## Data Model

Both sources are converted into a common schema:

| Field           | Description                                    |
| --------------- | ---------------------------------------------- |
| `source`        | Source website name                            |
| `source_url`    | URL associated with the scraped record         |
| `name_or_title` | Book title or quote text                       |
| `category`      | Category when available                        |
| `price`         | Numeric price when available                   |
| `rating`        | Standardized rating from 1 to 5 when available |
| `author`        | Author when available                          |
| `tags`          | Normalized tags when available                 |
| `description`   | Description when available                     |
| `scraped_at`    | UTC timestamp when the record was processed    |

Fields that are not available or not collected for a source are represented as null/empty values rather than invented data.

---

## Cleaning

Cleaning is implemented separately in `processing/cleaning.py`.

The cleaning process includes:

* Removing leading and trailing whitespace
* Normalizing repeated whitespace
* Handling non-breaking spaces
* Removing surrounding quote characters where appropriate
* Converting book prices to numeric values
* Converting ratings such as `One`, `Two`, `Three`, `Four`, and `Five` to numeric values
* Normalizing tags to lowercase
* Removing duplicate tags
* Sorting normalized tags

---

## Validation

Validation is implemented in `processing/validation.py`.

Records are checked for:

* Recognized source
* Required name/title
* Presence of source URL
* Valid HTTP/HTTPS URL format
* Non-negative numeric price
* Rating values between 1 and 5

Invalid records are rejected and logged instead of being included in the final dataset.

---

## Deduplication

Deduplication is implemented in `processing/deduplication.py`.

Exact string matching is not used as the only duplicate check. Values are normalized before generating a SHA-256 fingerprint.

### Books

Book duplicates are identified using:

* Source
* Normalized book title

### Quotes

Quote duplicates are identified using:

* Source
* Normalized author
* First 50 normalized characters of the quote

Duplicate records are removed from the final dataset and counted in the summary report.

---

## Error Handling and Reliability

The scraper includes handling for common failures such as:

* Connection errors
* Request exceptions
* HTTP errors
* Request timeouts
* Temporary server errors
* HTTP 429 responses
* Missing HTML elements
* Unexpected record-level parsing errors
* Invalid values

The base scraper retries selected temporary HTTP failures up to three times using increasing delays.

A request delay is also used between successful page requests.

If an individual record cannot be processed, the error is logged and the remaining records can continue processing.

If one source encounters an unexpected source-level failure, the other source can still be processed.

---

## Logging

Execution logs are written to:

```text
logs/scraper.log
```

The log contains information about:

* Scraping progress
* Request failures
* Retry attempts
* Invalid records
* Duplicate records
* Source-level errors
* Completion status

---

## Output

The pipeline generates:

### Final Dataset

```text
output/final_dataset.csv
```

This contains the consolidated and validated records from both sources.

### Summary Report

```text
output/summary_report.json
```

The summary contains source-level and overall processing statistics.

### Latest Successful Run

| Source           | Collected | After Cleaning | Rejected | Duplicates |    Final |
| ---------------- | --------: | -------------: | -------: | ---------: | -------: |
| Books to Scrape  |      1000 |           1000 |        0 |          1 |      999 |
| Quotes to Scrape |       100 |            100 |        0 |          0 |      100 |
| **Total**        |  **1100** |       **1100** |    **0** |      **1** | **1099** |

The final CSV contains **1099 data records** plus the header row, for a total of **1100 lines**.

---

## Tests

The project contains unit tests for:

* Cleaning
* Validation
* Deduplication

Run the tests with:

```bash
python -m pytest
```

Expected result:

```text
11 passed
```

Using `python -m pytest` ensures that the project package structure is correctly resolved.

---

## Assumptions

* The websites used are public scraping practice websites.
* The scraper does not attempt to bypass authentication, CAPTCHA, or other access controls.
* Pagination is followed through the website's `Next` link rather than hard-coded page numbers.
* Missing source-specific fields are represented as null/empty values.
* No data is invented when a field is unavailable.
* Duplicate books are identified using the normalized source and book title.
* Duplicate quotes are identified using the normalized source, author, and quote text fingerprint.
* The scraper uses a reasonable request delay.
* Temporary HTTP failures are retried.

---

## Known Limitations

* Category and description are not currently collected from the listing pages.
* Book availability is not currently included in the standardized dataset.
* Some source-specific fields are therefore represented as null values.
* The scraper depends on the current HTML structure of the practice websites. Changes to their HTML structure may require selector updates.
* For quotes, `source_url` currently stores the associated author URL rather than the individual quote page URL.
* The project was tested with Python 3.13.1, while the assignment recommends Python 3.10–3.12.

---

## AI Usage

ChatGPT was used as an AI coding assistant during development for:

* Project planning
* Python and web-scraping explanations
* Drafting implementation code
* Test creation
* Debugging
* Reviewing cleaning, validation, and deduplication logic
* Documentation

All AI-assisted code was reviewed, tested, and adjusted during development.

More detailed information about AI usage, representative prompts, changes made after reviewing AI output, and verification is available in:

```text
AI_USAGE.md
```

---

## Reproducibility

To reproduce the project:

```bash
pip install -r requirements.txt
python -m pytest
python main.py
```

After execution, check:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

The project does not require API keys, passwords, or other secrets.
