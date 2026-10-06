from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape",
}


def validate_record(record):
    errors = []

    source = record.get("source")
    name = record.get("name_or_title")
    source_url = record.get("source_url")
    price = record.get("price")
    rating = record.get("rating")

    if source not in VALID_SOURCES:
        errors.append("unknown_source")

    if not name:
        errors.append("missing_name")

    if not source_url:
        errors.append("missing_url")
    else:
        parsed_url = urlparse(source_url)

        if parsed_url.scheme not in ("http", "https"):
            errors.append("invalid_url")

    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            errors.append("invalid_price")

    if rating is not None:
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            errors.append("invalid_rating")

    return errors