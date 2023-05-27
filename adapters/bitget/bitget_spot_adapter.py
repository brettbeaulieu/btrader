import math
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pandas as pd

from adapters.base_adapter import BaseAdapter
from adapters.bitget.bitget_sdk.spot.market_api import MarketApi

from .const import Timeframes
from .utils import build_date_sequence


class BitgetSpotAdapter(BaseAdapter):
    def __init__(self, api_key, secret_key, passphrase):
        """Initialize the BitGetAdapter class."""
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__passphrase = passphrase
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

    def get_exchange(self):
        return "Bitget"

    def get_granularities(self) -> list[str]:
        return Timeframes.TF_SPOT

    def get_tickers(self) -> list[dict]:
        return self.api.tickers()["data"]

    def get_candles(
        self, symbol: str, granularity: str, start: datetime, end: datetime
    ) -> pd.DataFrame:
        """
        Retrieves kline data from the market API and returns it as a pandas dataframe.

        Args:
            symbol (str): The symbol to retrieve kline data for.
            granularity (str): The granularity of the kline data.
            start (datetime): The start time of the kline data.
            end (datetime): The end time of the kline data.
            limit (int): Maximum candles to retrieve per request (default 1000).
        Returns:
            pandas.DataFrame: A dataframe containing the kline data.
        """
        delta = Timeframes.DT_MAP[granularity]
        dates = build_date_sequence(start, end, delta)
        kline = []
        with ThreadPoolExecutor() as executor:
            for i in range(1, len(dates)):
                part = executor.submit(
                    self.get_candles_worker, symbol, granularity, dates[i - 1], dates[i]
                )
                kline.extend(part.result())

        # Create pandas dataframe from the kline
        kline = [x[0:6] for x in kline]
        df = pd.DataFrame(
            {
                "Time": pd.Series(
                    [pd.to_datetime(float(x[0]) * 1000000) for x in kline]
                ),
                "Open": pd.Series([x[1] for x in kline], dtype=float),
                "High": pd.Series([x[2] for x in kline], dtype=float),
                "Low": pd.Series([x[3] for x in kline], dtype=float),
                "Close": pd.Series([x[4] for x in kline], dtype=float),
                "Volume": pd.Series([x[5] for x in kline], dtype=float),
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
        """Worker function for retrieving kline data from the market API.
        Args:
            symbol (str): The symbol to retrieve kline data for.
            granul (str): The granularity of the kline data.
            start (datetime): The start time of the kline data.
            end (datetime): The end time of the kline data.
            limit (int): Maximum candles to retrieve per request (default 1000).
        Returns:
            list[list]: A list of lists containing the kline data.
        """
        kline = []
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
        kline.extend(vals)

        return kline

    def get_ticker_headers(self):
        return self.headers
