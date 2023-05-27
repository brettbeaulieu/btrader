""" Functions for obtaining a series of candles from a given exchange and pair"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from math import ceil

import pandas as pd

from bitget.mix.market_api import MarketApi as FuturesMarketAPI
from bitget.spot.market_api import MarketApi as SpotMarketAPI
from const import ProductType, Timeframes
from kline_info import KLineInfo


def build_date_sequence(info: KLineInfo, limit: int = 1000) -> list[datetime]:
    """Builds a list of datetimes for sequences of requests, used to ensure
    the total number of candles/request doesn't exceed the exchange's limit.
    Args:
        info (KLineInfo): Information about the kline to retrieve.
        limit (int): Maximum candles to retrieve per request (default 1000).
    Returns:
        list[datetime]: A list of datetimes for sequences of requests.
    """

    if limit > 1000:
        raise ValueError("Candle limit cannot be greater than 1000")

    # Calculate the number of intervals needed to get all the candles
    delta = Timeframes.DT_MAP[info.period]
    intervals = ceil((info.to - info.frm) / (delta * limit))

    # Add period * limit * i to the from date to get the next date
    dates = [info.frm + (i * delta * limit) for i in range(intervals)]
    # Manually add the to date to the end of the list to prevent overstepping it
    dates.append(info.to)

    return dates


def get_kline_dataframe(info: KLineInfo, limit: int = 1000):
    """
    Retrieves kline data from the market API and returns it as a pandas dataframe.

    Args:
        info (KLineInfo): Information about the kline to retrieve.
        limit (int): Maximum candles to retrieve per request (default 1000).
    Returns:
        pandas.DataFrame: A dataframe containing the kline data.
    """
    if limit > 1000:
        raise ValueError("Candle limit cannot be greater than 1000")
    if info.productType == ProductType.PT_SPOT:
        # TODO(me): Add API keys support
        marketAPI = SpotMarketAPI("", "", "")
    else:
        # TODO(me): Add API keys support
        marketAPI = FuturesMarketAPI("", "", "")

    dates = build_date_sequence(info, limit)
    infos = [
        KLineInfo(info.pair, info.period, info.productType, dates[i], dates[i + 1])
        for i in range(len(dates) - 1)
    ]
    kline = []

    with ThreadPoolExecutor() as executor:
        for worker_info in infos:
            part = executor.submit(get_kline_worker, marketAPI, worker_info, limit)
            kline.extend(part.result())

    # Create pandas dataframe from the kline
    kline = [x[0:6] for x in kline]
    df = pd.DataFrame(
        {
            "Time": pd.Series([pd.to_datetime(float(x[0]) * 1000000) for x in kline]),
            "Open": pd.Series([x[1] for x in kline], dtype=float),
            "High": pd.Series([x[2] for x in kline], dtype=float),
            "Low": pd.Series([x[3] for x in kline], dtype=float),
            "Close": pd.Series([x[4] for x in kline], dtype=float),
            "Volume": pd.Series([x[5] for x in kline], dtype=float),
        }
    )
    return df


def get_kline_worker(api, info: KLineInfo, limit: int = 1000) -> list[list]:
    """Worker function for retrieving kline data from the market API.
    Args:
       api (MarketAPI): The market API to use.
       info (KLineInfo): Information about the kline to retrieve.
       limit (int): Maximum candles to retrieve per request (default 1000).
    Returns:
       list[list]: A list of lists containing the kline data.
    """
    kline = []
    to_ms_og = str(int(info.to.timestamp() * 1000))
    delta = Timeframes.DT_MAP[info.period]
    # Get the from and to timestamps
    frm_ms = str(int(info.frm.timestamp() * 1000))
    to_ms = str(int((info.frm + limit * delta).timestamp() * 1000))

    # If the final 'to' timestamp is greater than the original 'to' timestamp,
    # set it to the original
    if to_ms > to_ms_og:
        to_ms = to_ms_og

    # Get candles
    if info.productType == ProductType.PT_SPOT:
        # Spot API returns a list of dictionaries, so we need to convert to a list of lists
        data = api.candles(
            info.pair + info.productType, info.period, frm_ms, to_ms, limit
        )["data"]
        vals = [list(x.values()) for x in data]
        kline.extend(vals)
    else:
        # Futures API returns a list of lists, so we can just extend kline
        kline.extend(
            api.candles(info.pair + info.productType, info.period, frm_ms, to_ms, limit)
        )
    info.frm += limit * delta
    return kline