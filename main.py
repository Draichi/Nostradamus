from nostradamus import Nostradamus

lucas = Nostradamus(from_symbol='BTC', to_symbol="USDT", histo="day", exchange="Binance", limit="200",
                    api_key="3d7d3e9e6006669ac00584978342451c95c3c78421268ff7aeef69995f9a09ce")

lucas.prophet(changepoint_prior_scale=0.02, forecast_days=13)
