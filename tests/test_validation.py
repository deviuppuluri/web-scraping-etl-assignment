from processing.validation import validate_record


def test_valid_book_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book_1/index.html",
        "name_or_title": "A Book",
        "price": 10.50,
        "rating": 4,
    }

    assert validate_record(record) == []


def test_missing_name():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": None,
        "price": 10.50,
        "rating": 4,
    }

    errors = validate_record(record)

    assert "missing_name" in errors


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "A Book",
        "price": 10.50,
        "rating": 7,
    }

    errors = validate_record(record)

    assert "invalid_rating" in errors