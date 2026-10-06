import re


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_text(value):
    if value is None:
        return None

    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    value = value.strip()

    return value if value else None


def strip_quotes(value):
    value = clean_text(value)

    if value is None:
        return None

    return value.strip('“”"')


def clean_price(value):
    if value is None:
        return None

    value = clean_text(value)

    if value is None:
        return None

    value = re.sub(r"[^\d.]", "", value)

    if not value:
        return None

    return float(value)


def clean_rating(value):
    if value is None:
        return None

    value = clean_text(value)

    if value is None:
        return None

    if value in RATING_MAP:
        return RATING_MAP[value]

    if value.isdigit():
        rating = int(value)

        if 1 <= rating <= 5:
            return rating

    return None


def clean_tags(tags):
    if not tags:
        return None

    cleaned_tags = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned_tags.append(tag.lower())

    cleaned_tags = sorted(set(cleaned_tags))

    return ";".join(cleaned_tags) if cleaned_tags else None