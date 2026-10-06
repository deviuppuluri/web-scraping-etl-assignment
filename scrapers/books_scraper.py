from urllib.parse import urljoin

from bs4 import BeautifulSoup

from processing.cleaning import clean_price, clean_rating, clean_text
from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    START_URL = "https://books.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:
            html = self.fetch_page(current_url)

            if html is None:
                self.logger.error(
                    "Stopping Books to Scrape because page failed: %s",
                    current_url,
                )
                break

            soup = BeautifulSoup(html, "lxml")

            books = soup.select("article.product_pod")

            for book in books:
                try:
                    title_element = book.select_one("h3 > a")
                    price_element = book.select_one("p.price_color")
                    rating_element = book.select_one("p.star-rating")
                    link_element = book.select_one("h3 > a[href]")

                    title = (
                        title_element.get("title")
                        if title_element
                        else None
                    )

                    price = (
                        price_element.get_text()
                        if price_element
                        else None
                    )

                    rating = None

                    if rating_element:
                        classes = rating_element.get("class", [])

                        for rating_word in [
                            "One",
                            "Two",
                            "Three",
                            "Four",
                            "Five",
                        ]:
                            if rating_word in classes:
                                rating = rating_word
                                break

                    book_url = (
                        urljoin(current_url, link_element.get("href"))
                        if link_element
                        else None
                    )

                    record = {
                        "source": "Books to Scrape",
                        "source_url": book_url,
                        "name_or_title": clean_text(title),
                        "category": None,
                        "price": clean_price(price),
                        "rating": clean_rating(rating),
                        "author": None,
                        "tags": None,
                        "description": None,
                        "scraped_at": None,
                    }

                    records.append(record)

                except Exception as error:
                    self.logger.warning(
                        "Failed to parse a book on %s: %s",
                        current_url,
                        error,
                    )

            next_link = soup.select_one("li.next > a")

            if next_link and next_link.get("href"):
                current_url = urljoin(
                    current_url,
                    next_link.get("href"),
                )
            else:
                current_url = None

        return records