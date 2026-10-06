from urllib.parse import urljoin

from bs4 import BeautifulSoup

from processing.cleaning import clean_text, clean_tags, strip_quotes
from scrapers.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:
            html = self.fetch_page(current_url)

            if html is None:
                self.logger.error(
                    "Stopping Quotes to Scrape because page failed: %s",
                    current_url,
                )
                break

            soup = BeautifulSoup(html, "lxml")

            quotes = soup.select("div.quote")

            for quote in quotes:
                try:
                    quote_element = quote.select_one("span.text")
                    author_element = quote.select_one("small.author")
                    tag_elements = quote.select("a.tag")

                    author_link = quote.select_one(
                        'a[href^="/author/"]'
                    )

                    quote_text = (
                        quote_element.get_text()
                        if quote_element
                        else None
                    )

                    author = (
                        author_element.get_text()
                        if author_element
                        else None
                    )

                    tags = [
                        tag.get_text()
                        for tag in tag_elements
                    ]

                    author_url = (
                        urljoin(
                            current_url,
                            author_link.get("href"),
                        )
                        if author_link
                        else None
                    )

                    record = {
                        "source": "Quotes to Scrape",
                        "source_url": author_url,
                        "name_or_title": strip_quotes(quote_text),
                        "category": None,
                        "price": None,
                        "rating": None,
                        "author": clean_text(author),
                        "tags": clean_tags(tags),
                        "description": None,
                        "scraped_at": None,
                    }

                    records.append(record)

                except Exception as error:
                    self.logger.warning(
                        "Failed to parse a quote on %s: %s",
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