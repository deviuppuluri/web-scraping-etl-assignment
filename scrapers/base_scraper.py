import logging
import time

import requests


class BaseScraper:
    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "ScrapingAssignment/1.0 (learning project)"
            }
        )

        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url):
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    response.encoding = "utf-8"
                    time.sleep(0.5)
                    return response.text

                if response.status_code in {429, 500, 502, 503, 504}:
                    wait_time = 2**attempt

                    self.logger.warning(
                        "Request failed with status %s for %s. "
                        "Retrying in %s seconds.",
                        response.status_code,
                        url,
                        wait_time,
                    )

                    time.sleep(wait_time)
                    continue

                self.logger.error(
                    "Request failed with status %s for %s",
                    response.status_code,
                    url,
                )

                return None

            except requests.RequestException as error:
                self.logger.warning(
                    "Request error for %s: %s",
                    url,
                    error,
                )

                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)

        self.logger.error("Failed to fetch page after retries: %s", url)

        return None