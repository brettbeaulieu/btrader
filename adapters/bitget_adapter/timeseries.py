import math
from candle import Candle

class DateRangeTooLargeError(Exception):
    """Raised when the number of 'getSeries' iterations is too large,
        and override is not enabled."""
    def __init__(self, message="Number of 'getSeries' iterations is too large, and override is not enabled."):
        self.message = message
        super().__init__(self.message)

class TimeSeries:
    def __init__(self, m: 'MarketApi'):
        self.api = m
    
    # ---- getSeries ----
    #   -- calculates number of iterations needed
    #   -- iterates get requests, builds chronological
    #   -- list of Candle objects. Returns the aforementioned list.
    def getSeries(self, symbol: str, granularity: str, startTime: str, endTime: str, override=False):
        iterations = 1
        num_candles = math.floor((int(endTime)-int(startTime))/(int(granularity)*1000))
        if num_candles > 100:
            if not override:
                raise DateRangeTooLargeError()
            iterations = math.ceil(num_candles/100)
            startTime = endTime - iterations*(1000*int(granularity)*100)
            endTime-= (iterations-1)*(1000*int(granularity)*100)
        
        series = []
        for x in range(0,iterations):
            candles = self.api.candles(symbol, granularity, startTime, endTime)
            for c in candles:
                if (c == None) or (c[1] == c[2] == c[3] == c[4]):
                    break
                series.append(Candle(c[0],c[1],c[2],c[3],c[4],c[5],c[6]))
            startTime = endTime
            endTime+=(1000*int(granularity)*100)

        series.reverse()
        return series

