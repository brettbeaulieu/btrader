

class Contract:
    def __init__(self, contract, ticker):
        self.contract = contract
        self.ticker = ticker 
        self.symbol = contract[0]
        self.maker = float(contract[1])
        self.taker = float(contract[2])
        self.feeRate = float(contract[3])
        self.openCost = float(contract[4])
        self.quote = contract[5]
        self.base = contract[6]
        self.buyRatio = float(contract[7])
        self.sellRatio = float(contract[8])
        self.marginCoins = contract[9]
        self.minTradeNum = float(contract[10])
        self.priceEndStep = float(contract[11])
        self.volumePlace = float(contract[12])
        self.pricePlace = float(contract[13])

        self.last = float(ticker[1])
        self.bestAsk = float(ticker[2])
        self.bestBid = float(ticker[3])
        self.high24h = float(ticker[4])
        self.low24h = float(ticker[5])
        self.timechecked = ticker[6]
        self.priceChange = float(ticker[7])
        self.baseVolume = float(ticker[8])
        self.quoteVolume = float(ticker[9])
        self.usdtVolume = float(ticker[10])
    
    def __getitem__(self, item):
        if item in self.contract:
            return self.contract[item]
        elif item in self.ticker:
            return self.ticker[item]
        else:
            raise KeyError("Key " +item +" could not be found.")

    def __str__(self):
        return ("Contract Info:"
        +"\n\tSymbol: " +self.symbol
        +"\n\tMaker Rate: " +str(self.maker*100) + "%"
        +"\n\tTaker Rate: " +str(self.taker*100) + "%" 
        +"\n\tFunding Rate: " +str(self.feeRate*100) + "%" 
        +"\n\tOpen Cost: " +str(self.openCost)
        +"\n\tQuote Coin: " +self.quote
        +"\n\tBase Coin: " +self.base
        +"\n\tBuy Ratio: " +str(self.buyRatio)
        +"\n\tSell Ratio: " +str(self.sellRatio) 
        +"\n\tMargin Coins: " +', '.join(self.marginCoins)
        +"\n\tMinimum Trade: " +str(self.minTradeNum) 
        +"\n\tPrice Step: " +str(self.priceEndStep)
        +"\n\tVolume Place: " +str(self.volumePlace)
        +"\n\tPrice Place: " +str(self.pricePlace)
        +"\nTicker Info:"
        +"\n\tLast: " +str(self.last)
        +"\n\tBest Ask: " +str(self.bestAsk)
        +"\n\tBest Bid: " +str(self.bestBid)
        +"\n\tHigh 24H: " +str(self.high24h)
        +"\n\tLow 24H: " +str(self.low24h)
        +"\n\tTime Updated: " +self.timechecked
        +"\n\tPercent Change: " +str(self.priceChange)
        +"\n\tBase Volume: " +str(self.baseVolume)
        +"\n\tQuote Volume: " +str(self.quoteVolume)
        +"\n\tUSDT Volume: $" +str(self.usdtVolume))




