from datetime import datetime, timedelta
from math import ceil
def build_date_sequence(startTime: datetime, endTime: datetime, delta: timedelta, limit: int = 1000) -> list[datetime]:
    """Builds a list of datetimes for sequences of requests, used to ensure
    the total number of candles/request doesn't exceed the exchange's limit.
    Args:
        startTime (datetime): Start time of the candle sequence.
        endTime (datetime): End time of the candle sequence.
        delta (timedelta): Time delta between each candle.
        limit (int): Maximum candles to retrieve per request (default 1000).
    Returns:
        list[datetime]: A list of datetimes for sequences of requests.
    """

    if limit > 1000:
        raise ValueError("Candle limit cannot be greater than 1000")

    # Calculate the number of intervals needed to get all the candles
    intervals = ceil((startTime - endTime) / (delta * limit))

    # Add period * limit * i to the from date to get the next date
    dates = [startTime + (i * delta * limit) for i in range(intervals)]
    
    # Manually add the to date to the end of the list to prevent overstepping it
    dates.append(endTime)
    return dates