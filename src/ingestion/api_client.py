import logging
import time

import httpx

from src.config.settings import settings


logger = logging.getLogger(__name__)


class CoinGeckoClient:
    def __init__(self):
        self.base_url = settings.coingecko_base_url

    def get_market_data(
        self,
        coin_ids: list[str],
        vs_currency: str = "usd",
        max_retries: int = 3,
    ) -> list[dict]:

        params = {
            "vs_currency": vs_currency,
            "ids": ",".join(coin_ids),
        }

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    "Requesting CoinGecko | attempt=%d/%d",
                    attempt,
                    max_retries,
                )

                response = httpx.get(
                    f"{self.base_url}/coins/markets",
                    params=params,
                    timeout=10,
                )

                response.raise_for_status()

                logger.info(
                    "CoinGecko request successful | status=%d",
                    response.status_code,
                )

                return response.json()

            except httpx.HTTPError as error:
                logger.warning(
                    "CoinGecko request failed | attempt=%d/%d | error=%s",
                    attempt,
                    max_retries,
                    error,
                )

                if attempt == max_retries:
                    logger.error(
                        "CoinGecko request failed after %d attempts",
                        max_retries,
                    )
                    raise

                time.sleep(2 ** (attempt - 1))