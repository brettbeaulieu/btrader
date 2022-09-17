import asyncio
import time
import math

from bitget.mix.market_api import MarketApi
from timeseries_asynch import TimeSeriesAsynch


m = MarketApi(
    "bg_0d456f8fe40db4bcfc8300b4e6242b75",
    "74de60c68c9ea07d20b13aa0c6d849668810fcb71993434a33469f65fc71152b",
    "meyerClaire30",
    use_server_time=False,
    first=False,
)
z = TimeSeriesAsynch(m)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

startTime = time.time()
adjTime = math.floor(startTime) * 1000
timeframe = 60
candleswanted = 3000
difference = timeframe * candleswanted * 1000
series = asyncio.run(
    z.getSeries(
        "BTCUSDT_UMCBL", str(timeframe), adjTime - difference, int(adjTime), True
    )
)
duration = time.time() - startTime

f = open("myfile.txt", "w",encoding="utf-8")
leng = 0
for x in series:
    for candle in x:
        f.write(str(candle) + "\n")
        leng += 1
print("Asynchronous Get Complete.")
print("Time Elapsed: ", duration, " seconds.")
print("Total Candles: ", str(leng))
print("Rate: ", str(leng / duration), " candles per second.")
f.close()
