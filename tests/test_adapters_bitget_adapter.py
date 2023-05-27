import unittest
from datetime import datetime, timedelta

import pandas as pd

from adapters.bitget.bitget_spot_adapter import BitgetSpotAdapter


class Test_BitgetSpotAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = BitgetSpotAdapter("", "", "")

    def test_get_exchange(self):
        assert self.adapter.get_exchange() == "Bitget"

    def test_get_candles(self):
        today = datetime.today()
        assert isinstance(
            self.adapter.get_candles("BTCUSDT", "1m", today - timedelta(days=1), today),
            pd.DataFrame,
        )

    def test_get_symbols(self):
        raise NotImplementedError

    def test_get_granularities(self):
        assert isinstance(self.adapter.get_granularities(), list)

    def test_get_ticker(self):
        # TODO: implement this
        raise NotImplementedError

    def test_get_ticker_headers(self):
        assert isinstance(self.adapter.get_ticker_headers(), dict)
