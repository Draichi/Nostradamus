from nostradamus import Nostradamus
import os

API_KEY = os.environ.get('API_KEY')

FORECAST_DAYS = 80
HISTO = "day"  # "day" | "hour"
LIMIT = "250"  # number of days/hours
CHANGEPOINTS_PRIOR_SCALE = [
    0.04,
    0.1,
    # 0.25,
]

ASSETS = [
    # 'aave',
    # 'link',
    # 'btc',
    # 'crv',
    # 'snx',
    'eth',
    # 'sushi',
    # 'matic'
]

for asset in ASSETS:
    print("> {}".format(asset))

    tmp = Nostradamus(from_symbol=asset,
                      to_symbol="usd",
                      histo=HISTO,
                      limit=LIMIT,
                      api_key=API_KEY)

    for changepoint_prior_scale in CHANGEPOINTS_PRIOR_SCALE:
        tmp.prophet(changepoint_prior_scale=changepoint_prior_scale,
                    forecast_days=FORECAST_DAYS)
