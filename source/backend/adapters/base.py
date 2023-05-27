import pandas as pd
from datetime import datetime


class BaseAdapter:
    ''' Base class for all adapters. '''
    def __init__(self, exchange: str):
        self.exchange = "Base Name"

    def get_exchange(self) -> str:
        ''' Get the exchange name. '''
        raise NotImplementedError("Base Adapter get_exchange() called. Override this method in the child class.")

    def get_candles(self, symbol: str, granularity: str, startTime: datetime, endTime: datetime) -> pd.DataFrame:
        ''' Get candles from the exchange. '''
        raise NotImplementedError("Base Adapter get_candles() called. Override this method in the child class.")
    
    def get_symbols(self) -> list[str]:
        ''' Get symbols from the exchange. '''
        raise NotImplementedError("Base Adapter get_symbols() called. Override this method in the child class.")
    
    def get_granularities(self) -> list[str]:
        ''' Get granularities supported by the exchange. Also known as intervals or periods.'''
        raise NotImplementedError("Base Adapter get_granularities() called. Override this method in the child class.")

    def get_ticker(self, symbol: str) -> dict[str, str]:
        ''' Get data for a given ticker from the exchange. '''
        raise NotImplementedError("Base Adapter get_ticker() called. Override this method in the child class.")
    
    def get_ticker_headers(self) -> dict[str, str]:
        ''' Get the headers for the ticker data. '''
        raise NotImplementedError("Base Adapter get_ticker_headers() called. Override this method in the child class.")
