
Candles
========================================
The Candle class allows for storing OHLC price data, as well as time 
and volume data. 

Methods
-------

Candle.\ **priceKeys**\(self)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Returns a list of price-related index keys for candle objects.

Candle.\ **keys**\(self)
--------------------------
Returns a list of all possible candle object index keys.

Candle.\ **__setitem__**\(self, inputCandle)
--------------------------------------------
Description

Candle.\ **__getitem__**\(self, inputCandle)
--------------------------------------------
Description

Candle.\ **__str__**\(self)
---------------------------
Returns a string representation of the object.

Candle.\ **__sub__**\(self, inputCandle)
----------------------------------------
Return a candle object storing the difference between candle 'self' and candle 'inputCandle'

Candle.\ **__add__**\(self, inputCandle)
----------------------------------------
Return a candle object storing respective sums of candle 'self' and candle 'inputCandle' data


.. code-block:: python
   
   c = Candle()
   print(c['quote'])
   >>> 0



