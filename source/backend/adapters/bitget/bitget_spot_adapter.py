from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd

from ..base import BaseAdapter
from .bitget_sdk.spot.market_api import MarketApi
from .const import Timeframes
from .utils import build_date_sequence


class BitgetSpotAdapter(BaseAdapter):
    """Adapter for the Bitget spot market API.

    Attributes:
        api (MarketApi): The Bitget spot market API.
        headers (dict): A dictionary mapping column names to their display names.
    """

    def __init__(self, api_key, secret_key, passphrase):
        """Initialize the BitgetSpotAdapter class."""
        self.api = MarketApi(api_key, secret_key, passphrase)
        self.headers = {
            "symbol": "Symbol",
            "high24h": "24H High",
            "low24h": "24H Low",
            "close": "Close Price",
            "quoteVol": "Quote Volume",
            "baseVol": "Base Volume",
            "usdtVol": "USDT Volume",
            "ts": "Time",
            "buyOne": "Buy One",
            "sellOne": "Sell One",
            "bidSz": "Bid Size",
            "askSz": "Ask Size",
            "openUtc0": "Open UTC",
            "changeUtc": "Change UTC",
            "change": "% Change",
        }

    def get_exchange(self) -> str:
        """
        Returns the name of the exchange.
        
        Returns:
            str: The name of the exchange."""
        return "Bitget"

    def get_granularities(self) -> list[str]:
        """Returns a list of supported granularities/periods.

        Returns:
            list[str]: A list of supported granularities/periods."""
        return Timeframes.TF_SPOT
    
    def get_symbols(self) -> list[str]:
        """
        Returns a list of all symbols offered by the exchange.

        Returns:
            list[str]: A list of all symbols.
        """
        return super().get_symbols()

    def get_tickers(self) -> list[dict]:
        """
        Returns a list of all tickers offered by the exchange.
        
        Returns:
            list[dict]: A list of all tickers.
        """
        return self.api.tickers()["data"]

    def get_candles(
        self, symbol: str, granularity: str, start: datetime, end: datetime
    ) -> pd.DataFrame:
        """
        Retrieves a candlestick series from the market API, and returns it as a pandas dataframe.

        Parameters:
            symbol (str): The symbol to retrieve a candlestick series for.
            granularity (str): The granularity/period of the candlesticks.
            start (datetime): The start time of the candlestick series.
            end (datetime): The end time of the candlestick series.
            limit (int): Maximum candles to retrieve per request (default 1000).
        Returns:
            pandas.DataFrame: A dataframe containing the candlestick series.
        """
        delta = Timeframes.DT_MAP[granularity]
        dates = build_date_sequence(start, end, delta)
        candlestick = []
        with ThreadPoolExecutor() as executor:
            for i in range(1, len(dates)):
                part = executor.submit(
                    self.get_candles_worker, symbol, granularity, dates[i - 1], dates[i]
                )
                candlestick.extend(part.result())

        # Create pandas dataframe from the candlestick
        candlestick = [x[0:6] for x in candlestick]
        df = pd.DataFrame(
            {
                "Time": pd.Series(
                    [pd.to_datetime(float(x[0]) * 1000000) for x in candlestick]
                ),
                "Open": pd.Series([x[1] for x in candlestick], dtype=float),
                "High": pd.Series([x[2] for x in candlestick], dtype=float),
                "Low": pd.Series([x[3] for x in candlestick], dtype=float),
                "Close": pd.Series([x[4] for x in candlestick], dtype=float),
                "Volume": pd.Series([x[5] for x in candlestick], dtype=float),
            }
        )
        return df

    def get_candles_worker(
        self,
        symbol: str,
        granul: str,
        start: datetime,
        end: datetime,
        limit: int = 1000,
    ) -> list[list]:
        """
        Worker function for retrieving candlestick data from the market API.
        
        Args:
            symbol (str): The symbol to retrieve a candlestick series for.
            granul (str): The granularity/period of the candlesticks.
            start (datetime): The start time of the candlestick series.
            end (datetime): The end time of the candlestick series.
            limit (int): Maximum candles to retrieve per request (default 1000).
        Returns:
            list[list]: A list of lists representing the candlestick series.
        """
        candlestick = []
        delta = Timeframes.DT_MAP[granul]
        to_ms_og = str(int(start.timestamp() * 1000))
        # Get the from and to timestamps
        frm_ms = str(int(end.timestamp() * 1000))
        to_ms = str(int((end + limit * delta).timestamp() * 1000))

        # If the final 'to' timestamp is greater than the original 'to' timestamp,
        # set it to the original
        if to_ms > to_ms_og:
            to_ms = to_ms_og

        # Spot API returns a list of dictionaries, so we need to convert to a list of lists
        data = self.api.candles(symbol, granul, frm_ms, to_ms, limit)["data"]
        data = data["data"]
        vals = [list(x.values()) for x in data]
        candlestick.extend(vals)

        return candlestick

    def get_ticker_headers(self):
        return self.headers
