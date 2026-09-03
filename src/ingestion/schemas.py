from datetime import datetime

from pydantic import BaseModel, Field


class MarketRecord(BaseModel):
    symbol: str = Field(min_length=1)
    current_price: float = Field(ge=0)
    last_updated: datetime