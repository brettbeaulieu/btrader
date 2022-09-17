
from datetime import datetime
class Candle:

    def __init__(self, t:float=0, o:float=0, h:float=0, l:float=0, c:float=0, b:float=0, q:float=0):
        """ T -> Time, O -> Open, H -> High, L -> Low, C -> Close, B -> BaseVol, Q -> QuoteVol """
        self.t = t
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.b = b
        self.q = q
    
    def priceKeys(self): return ['Open','High','Low','Close']
    def keys(self): return ['Time','Open','High','Low','Close','BaseVol','QuoteVol']
    
    def __setitem__(self, itemName, itemValue):
        match itemName.lower():
            case "t" | "time":
                self.t = itemValue
            case "o" | "open":
                self.o = itemValue 
            case "h" | "high":
                self.h = itemValue 
            case "l" | "low":
                self.l = itemValue 
            case "c" | "close":
                self.c = itemValue 
            case "b" | "basevol":
                self.b = itemValue 
            case "q" | "quotevol":
                self.q = itemValue   
            case _:
                raise KeyError()
    
    def __getitem__(self, itemName):

        match itemName.lower():
            case "t" | "time":
                return self.t
            case "o" | "open":
                return self.o 
            case "h" | "high":
                return self.h
            case "l" | "low":
                return self.l
            case "c" | "close":
                return self.c
            case "b" | "basevol":
                return self.b
            case "q" | "quotevol":
                return self.q       
            case _:
                raise KeyError()

        
    def __str__(self):
        return ("Candle @ " + str(datetime.fromtimestamp(int(self.t)/1000))
                +"\nOpen: $" +str(self.o) +"\nClose: $" +str(self.c)
                +"\nHigh: $" +str(self.h) +"\nLow: $" +str(self.l) 
                +"\nBase Volume: " +str(self.b) +"\nQuote Volume: "
                +str(self.q) + "\n")

    # TODO: Add type hinting somehow
    def __sub__(self, inputCandle):
        if not isinstance(inputCandle,Candle):
            raise TypeError()
        if inputCandle == self:
            return Candle()

        newCandle = Candle()
        for data in self.keys():
            newCandle[data] = self[data]-inputCandle[data]
        return newCandle
    
    def __add__(self,inputCandle):
        if not isinstance(inputCandle,Candle):
            raise TypeError()
        if inputCandle == self:
            return Candle()
        
        newCandle = Candle()
        for data in self.keys():
            newCandle[data] = self[data]+inputCandle[data]
        return newCandle