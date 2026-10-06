import hashlib
import re


def normalize_for_fingerprint(value):
    if value is None:
        return ""

    value = str(value).lower()
    value = re.sub(r"[^\w\s]", "", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def create_fingerprint(record):
    source = normalize_for_fingerprint(record.get("source"))

    if source == "books to scrape":
        identifying_value = normalize_for_fingerprint(
            record.get("name_or_title")
        )

    else:
        author = normalize_for_fingerprint(record.get("author"))
        quote = normalize_for_fingerprint(record.get("name_or_title"))

        identifying_value = f"{author}|{quote[:50]}"

    raw_value = f"{source}|{identifying_value}"

    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def remove_duplicates(records):
    unique_records = []
    seen = set()
    duplicate_count = 0

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_count += 1
            continue

        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count