from datetime import timedelta


class Timeframes:
    """Enumeration of granularity timeframes for Bitget API candlestick data"""

    TF_SPOT_1m = "1min"  # 1 minute
    TF_SPOT_5m = "5min"  # 5 minute
    TF_SPOT_15m = "15min"  # 15 minute
    TF_SPOT_30m = "30min"  # 30 minute
    TF_SPOT_1D = "1day"  # 1 day
    TF_SPOT_3D = "3day"  # 3 day
    TF_SPOT_1W = "1week"  # Weekly
    TF_1m = "1m"  # 1 minute
    TF_5m = "5m"  # 5 minute
    TF_15m = "15m"  # 15 minute
    TF_30m = "30m"  # 30 minute
    TF_1H = "1H"  # 1 hour
    TF_4H = "4H"  # 4 hour
    TF_6H = "6H"  # 6 hour
    TF_12H = "12H"  # 12 hour
    TF_1D = "1D"  # 1 day
    TF_1W = "1W"  # Weekly
    TF_1M = "1M"  # Monthly
    TF_UTC_6H = "6Hutc"  # UTC0 6 hour
    TF_UTC_12H = "12Hutc"  # UTC0 12 hour
    TF_UTC_1D = "1Dutc"  # UTC0 1 day
    TF_UTC_3D = "3Dutc"  # UTC0 3 day
    TF_UTC_1W = "1Wutc"  # UTC0 Weekly
    TF_UTC_1M = "1Mutc"  # UTC0 Monthly
    TF_FUTURES = [
        TF_1m,
        TF_5m,
        TF_15m,
        TF_30m,
        TF_1H,
        TF_4H,
        TF_6H,
        TF_12H,
        TF_1D,
        TF_1W,
        TF_1M,
        TF_UTC_6H,
        TF_UTC_12H,
        TF_UTC_1D,
        TF_UTC_3D,
        TF_UTC_1W,
        TF_UTC_1M,
    ]
    TF_SPOT = [
        TF_SPOT_1m,
        TF_SPOT_5m,
        TF_SPOT_15m,
        TF_SPOT_30m,
        TF_SPOT_1D,
        TF_SPOT_3D,
        TF_SPOT_1W,
    ]
    TF_ALL = [
        TF_SPOT_1m,
        TF_SPOT_5m,
        TF_SPOT_15m,
        TF_SPOT_30m,
        TF_SPOT_1D,
        TF_SPOT_3D,
        TF_SPOT_1W,
        TF_1m,
        TF_5m,
        TF_15m,
        TF_30m,
        TF_1H,
        TF_4H,
        TF_6H,
        TF_12H,
        TF_1D,
        TF_1W,
        TF_1M,
        TF_UTC_6H,
        TF_UTC_12H,
        TF_UTC_1D,
        TF_UTC_3D,
        TF_UTC_1W,
        TF_UTC_1M,
    ]
    DT_MAP = {  # Map timeframes to timedelta objects
        TF_SPOT_1m: timedelta(minutes=1),
        TF_SPOT_5m: timedelta(minutes=5),
        TF_SPOT_15m: timedelta(minutes=15),
        TF_SPOT_30m: timedelta(minutes=30),
        TF_SPOT_1D: timedelta(days=1),
        TF_SPOT_3D: timedelta(days=3),
        TF_SPOT_1W: timedelta(weeks=1),
        TF_1m: timedelta(minutes=1),
        TF_5m: timedelta(minutes=5),
        TF_15m: timedelta(minutes=15),
        TF_30m: timedelta(minutes=30),
        TF_1H: timedelta(hours=1),
        TF_4H: timedelta(hours=4),
        TF_6H: timedelta(hours=6),
        TF_12H: timedelta(hours=12),
        TF_1D: timedelta(days=1),
        TF_1W: timedelta(weeks=1),
        TF_1M: timedelta(days=30),  # Approximate, not exact TODO(me): Fix this
        TF_UTC_6H: timedelta(hours=6),
        TF_UTC_12H: timedelta(hours=12),
        TF_UTC_1D: timedelta(days=1),
        TF_UTC_3D: timedelta(days=3),
        TF_UTC_1W: timedelta(weeks=1),
        # Approximate, not exact TODO(me): Fix this
        TF_UTC_1M: timedelta(days=30),
    }


class ProductType:
    """Enumeration of product types for the Bitget API"""

    PT_SPOT = "_SPBL"  # Spot
    PT_USDT_PERP = "_UMCBL"  # USDT perpetual contract
    PT_UNIV_PERP = "_DMCBL"  # Universal margin perpetual contract
    PT_USDC_PERP = "_CMCBL"  # USDC perpetual contract
    PT_SIM_USDT_PERP = "_SUMCBL"  # Simulated USDT perpetual contract
    PT_SIM_UNIV_PERP = "_SDMCBL"  # Simulated Universal margin perpetual contract
    PT_SIM_USDC_PERP = "_SCMSBL"  # Simulated USDC perpetual contract
    PT_ALL = [
        PT_SPOT,
        PT_USDT_PERP,
        PT_UNIV_PERP,
        PT_USDC_PERP,
        PT_SIM_USDT_PERP,
        PT_SIM_UNIV_PERP,
        PT_SIM_USDC_PERP,
    ]
