from nostradamus import Nostradamus

env = Nostradamus(from_symbol='eth', to_symbol="USDT", histo="day", exchange="Binance", limit="250",
                    api_key="")

env.prophet(changepoint_prior_scale=0.08, forecast_days=30)
