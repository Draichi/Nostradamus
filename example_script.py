from nostradamus import Nostradamus
import os

API_KEY = os.environ.get('API_KEY')

env = Nostradamus(from_symbol='eth',
                  to_symbol="USDT",
                  histo="day",
                  limit="250",
                  api_key=API_KEY)

env.prophet(changepoint_prior_scale=0.08,
            forecast_days=30)
