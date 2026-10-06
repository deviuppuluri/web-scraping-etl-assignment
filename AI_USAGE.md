# AI Usage

## Tools Used

ChatGPT was used as an AI coding assistant during development.

## How AI Was Used

AI assistance was used for:

* Planning the project structure
* Designing the scraping pipeline
* Drafting Python functions
* Explaining Python and web-scraping concepts
* Creating unit tests
* Debugging import and tes
t-running issues
* Reviewing validation and deduplication logic
* Preparing project documentation

## Representative Prompts

Examples of prompts used during development included:

* Help me build this web scraping assignment step by step.
* Explain how to implement pagination using the Next link.
* Help create cleaning functions for price, rating, whitespace, and tags.
* Help implement validation and duplicate detection.
* Help debug a `ModuleNotFoundError` when running pytest.
* Help verify that the CSV and summary JSON counts reconcile.

## AI-Assisted Code

AI assistance was used to draft portions of:

* `scrapers/base_scraper.py`
* `scrapers/books_scraper.py`
* `scrapers/quotes_scraper.py`
* `processing/cleaning.py`
* `processing/validation.py`
* `processing/deduplication.py`
* `main.py`
* Unit tests

The generated code was reviewed and tested in the local development environment.

## Review and Changes

The implementation was reviewed while running the project.

An issue occurred when running `pytest` directly:

```text
ModuleNotFoundError: No module named 'processing'
```

The tests were successfully executed using:

```bash
python -m pytest
```

This produced:

```text
11 passed
```

## Changes Made After Reviewing AI Output

The AI-generated implementation was reviewed and tested rather than used blindly.

One issue occurred when running the tests using:

```bash
pytest
```

This resulted in:

```text
ModuleNotFoundError: No module named 'processing'
```

The test command was changed to:

```bash
python -m pytest
```

After this change, all tests passed successfully:

```text
11 passed
```

The scraping implementation was also tested by running:

```bash
python main.py
```

The scraper completed successfully and produced 1099 final records.

Some fields such as category and description are left as null when they are not collected from the source pages. This avoids inventing data and avoids unnecessary detail-page requests. These limitations are documented in the README.

## Incorrect or Incomplete AI Suggestions

During development, some generated approaches required adjustment after testing.

In particular, the initial direct `pytest` command did not correctly resolve the project packages in the local environment. Running pytest through the Python module interface solved the issue.

All AI-assisted code was reviewed, executed, tested, and adjusted before being included in the final project.

## Verification

The implementation was verified through:

1. Unit tests
2. A complete scraper run
3. Checking the generated CSV
4. Checking the generated summary JSON
5. Checking the generated log file
6. Comparing summary counts with CSV row counts

The final CSV contained 1099 data records.

The summary reported:

* 999 final book records
* 100 final quote records
* 1099 total final records

The CSV contained 1100 lines including the header, confirming that the summary and CSV counts reconcile.

## Understanding

The final implementation was reviewed during development so that the scraping flow, pagination, cleaning, validation, deduplication, error handling, and output generation can be explained and maintained by the developer.
