import csv
import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from processing.deduplication import remove_duplicates
from processing.validation import validate_record
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper


OUTPUT_DIR = Path("output")
LOG_DIR = Path("logs")

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"

FIELDNAMES = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def add_scraped_time(records):
    scraped_at = datetime.now(timezone.utc).isoformat()

    for record in records:
        record["scraped_at"] = scraped_at

    return records


def write_csv(records):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(records)


def write_summary(summary):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
        )


def process_source(name, records):
    cleaned_count = len(records)
    rejected_count = 0
    rejection_reasons = Counter()
    valid_records = []

    for record in records:
        errors = validate_record(record)

        if errors:
            rejected_count += 1

            for error in errors:
                rejection_reasons[error] += 1

            logging.warning(
                "Rejected record from %s: %s",
                name,
                errors,
            )

            continue

        valid_records.append(record)

    unique_records, duplicate_count = remove_duplicates(
        valid_records
    )

    stats = {
        "records_collected": len(records),
        "records_cleaned": cleaned_count,
        "records_rejected": rejected_count,
        "rejected_by_reason": dict(rejection_reasons),
        "duplicates_removed": duplicate_count,
        "final_records": len(unique_records),
    }

    return unique_records, stats


def main():
    setup_logging()

    start_time = datetime.now(timezone.utc)

    logging.info("Scraping job started")

    all_records = []
    source_stats = {}

    scrapers = [
        ("Books to Scrape", BooksScraper()),
        ("Quotes to Scrape", QuotesScraper()),
    ]

    for source_name, scraper in scrapers:
        logging.info("Starting source: %s", source_name)

        try:
            records = scraper.scrape()
            records = add_scraped_time(records)

            processed_records, stats = process_source(
                source_name,
                records,
            )

            all_records.extend(processed_records)
            source_stats[source_name] = stats

            logging.info(
                "Finished %s: %s final records",
                source_name,
                stats["final_records"],
            )

        except Exception as error:
            logging.exception(
                "Unexpected error while processing %s: %s",
                source_name,
                error,
            )

            source_stats[source_name] = {
                "records_collected": 0,
                "records_cleaned": 0,
                "records_rejected": 0,
                "rejected_by_reason": {},
                "duplicates_removed": 0,
                "final_records": 0,
                "error": str(error),
            }

    write_csv(all_records)

    end_time = datetime.now(timezone.utc)

    duration = (end_time - start_time).total_seconds()

    total_collected = sum(
        stats["records_collected"]
        for stats in source_stats.values()
    )

    total_cleaned = sum(
        stats["records_cleaned"]
        for stats in source_stats.values()
    )

    total_rejected = sum(
        stats["records_rejected"]
        for stats in source_stats.values()
    )

    total_duplicates = sum(
        stats["duplicates_removed"]
        for stats in source_stats.values()
    )

    summary = {
        "run": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
        },
        "sources": source_stats,
        "totals": {
            "records_collected": total_collected,
            "records_cleaned": total_cleaned,
            "records_rejected": total_rejected,
            "duplicates_removed": total_duplicates,
            "final_records": len(all_records),
        },
    }

    write_summary(summary)

    logging.info(
        "Scraping job finished with %s final records",
        len(all_records),
    )

    print("Scraping job completed successfully.")
    print(f"Final records: {len(all_records)}")
    print(f"CSV: {CSV_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()