import httpx

from src.config.settings import settings


class CoinGeckoClient:
    def __init__(self):
        self.base_url = settings.coingecko_base_url

    def get_market_data(
        self,
        coin_ids: list[str],
        vs_currency: str = "usd",
    ) -> list[dict]:
        params = {
            "vs_currency": vs_currency,
            "ids": ",".join(coin_ids),
        }

        response = httpx.get(
            f"{self.base_url}/coins/markets",
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()