from processing.deduplication import remove_duplicates


def test_duplicate_books_are_removed():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "The Great Book",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "  THE GREAT BOOK  ",
        },
    ]

    unique_records, duplicate_count = remove_duplicates(records)

    assert len(unique_records) == 1
    assert duplicate_count == 1


def test_unique_books_are_kept():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Book One",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Book Two",
        },
    ]

    unique_records, duplicate_count = remove_duplicates(records)

    assert len(unique_records) == 2
    assert duplicate_count == 0