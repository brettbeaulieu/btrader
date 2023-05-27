
def getContractsInfo(mAPI, types):
    return mAPI.contracts(types)["data"]

def getTickersInfo(mAPI, types):
    return mAPI.tickers(types)["data"]

def getAllInfo(mAPI, types):
    contractsInfo = mAPI.contracts(types)["data"]
    tickersInfo = mAPI.tickers(types)["data"]
    for x in range(0, len(contractsInfo)):
        tickersInfo[x] = contractsInfo[x] | tickersInfo[x]
    return tickersInfo

def getAllSymbols(mAPI, types):
    return [x["symbol"].split("_")[0] for x in mAPI.tickers(types)["data"]]
