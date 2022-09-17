import math
import aiohttp
from aiolimiter import AsyncLimiter
import asyncio

from bitget.mix.market_api import MarketApi
from candle import Candle
from bitget import consts as c, utils


class DateRangeTooLargeError(Exception):
    """Raised when the number of 'getSeries' iterations is too large,
    and override is not enabled."""

    def __init__(
        self,
        message="Number of 'getSeries' iterations is too large, and override is not enabled.",
    ):
        self.message = message
        super().__init__(self.message)


class TimeSeriesAsynch:
    def __init__(self, m: MarketApi):
        self.api = m

    async def candles_async(self, session, path):
        # ---- Create Request Parameters
        timestamp = utils.get_timestamp()
        sign = utils.sign(
            utils.pre_hash(timestamp, c.GET, path, ""), self.api.API_SECRET_KEY
        )
        header = utils.get_header(
            self.api.API_KEY, str(sign), str(timestamp), self.api.PASSPHRASE
        )
        url = "https://api.bitget.com/api/mix/v1/market/candles" + path
        async with session.get(url, headers=header) as resp:
            series = []
            candles = await resp.json()
            for x in candles:
                if (x == None) or (x[1] == x[2] == x[3] == x[4]):
                    break
                series.append(Candle(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
            return series

    # ---- getSeries ----
    #   -- calculates number of iterations needed
    #   -- iterates get requests, builds chronological
    #   -- list of Candle objects. Returns the aforementioned list.
    async def getSeries(
        self, symbol, granularity, startTime="", endTime="", override=False
    ):
        # ---- Calculate number of candles, and required iterations.
        iterations = 1
        num_candles = math.floor(
            (int(endTime) - int(startTime)) / (int(granularity) * 1000)
        )
        if num_candles > 100:
            if not override:
                raise DateRangeTooLargeError()
            iterations = math.ceil(num_candles / 100)
            startTime = endTime - iterations * (1000 * int(granularity) * 100)
            endTime -= (iterations - 1) * (1000 * int(granularity) * 100)
        # ---- build http client
        limiter = AsyncLimiter(18, 1)
        client = aiohttp.ClientSession()
        async with client as session:
            # ---- Fetch candles, append each tempSeries to finalSeries
            finalSeries = []
            tempSeries = []
            for x in range(0, iterations):
                path = "?symbol=" + str(symbol) + "&granularity=" + str(granularity)
                path = (
                    path + "&startTime=" + str(startTime) + "&endTime=" + str(endTime)
                )
                tempSeries.append(
                    asyncio.ensure_future(self.candles_async(session, path))
                )
                startTime = endTime
                endTime += 1000 * int(granularity) * 100
                await asyncio.sleep(1 / 20)
            finalSeries = await asyncio.gather(*tempSeries)
        return finalSeries
