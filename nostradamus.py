import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as offline
import fbprophet
import os
import requests
from termcolor import colored
from yaspin import yaspin
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({
    'msg': '#4caf50 bold',
    'sub-msg': '#616161 italic'
})


class Nostradamus:
    def __init__(self, from_symbol, to_symbol, histo, exchange, limit, api_key):
        self.from_symbol = from_symbol
        self.to_symbol = to_symbol
        self.histo = histo
        self.exchange = exchange
        self.limit = limit
        self.api_key = api_key
        self.df = self.get_datasets()

    def prophet(self, forecast_days, changepoint_prior_scale=0.05):
        df = pd.DataFrame(self.df)
        df_prophet = fbprophet.Prophet(
            changepoint_prior_scale=changepoint_prior_scale,
            daily_seasonality=True)
        df_prophet.fit(df)
        df_forecast = df_prophet.make_future_dataframe(
            periods=int(forecast_days))
        forecast = df_prophet.predict(df_forecast)
        forecast.to_csv('datasets/forecast.csv')
        self.plot_datasets(forecast)

    def get_datasets(self):
        dataset_path = 'datasets/{}_{}_{}.csv'.format(self.from_symbol +
                                                      self.to_symbol, self.limit, self.histo)
        if not os.path.exists(dataset_path):
            headers = {'User-Agent': 'Mozilla/5.0',
                       'authorization': 'Apikey {}'.format(self.api_key)}
            url = 'https://min-api.cryptocompare.com/data/histo{}?fsym={}&tsym={}&e={}&limit={}'.format(
                self.histo, self.from_symbol.upper(), self.to_symbol.upper(), self.exchange, self.limit)
            with yaspin(text='Downloading {}/{}'.format(self.from_symbol, self.to_symbol)) as sp:
                response = requests.get(url, headers=headers)
                sp.hide()
                print_formatted_text(HTML(
                    u'<b>></b> <msg>{} {} {}(s)</msg> <sub-msg>download complete</sub-msg>'.format(
                        self.from_symbol + self.to_symbol, self.limit, self.histo)
                ), style=style)
                sp.show()
                sp.ok()
            json_response = response.json()
            status = json_response['Response']
            if status == "Error":
                print(colored('=== {} ==='.format(
                    json_response['Message']), 'red'))
                raise AssertionError()
            result = json_response['Data']
            df = pd.DataFrame(result)
            df['Date'] = pd.to_datetime(df['time'], utc=True, unit='s')
            df['ds'] = df['Date'].dt.date
            df['y'] = df['close']
            df.drop('time', axis=1, inplace=True)
            df.dropna(inplace=True)
            df = df[['y', 'ds']]
            df.to_csv(dataset_path)
            return df
        else:
            df = pd.read_csv(dataset_path)
            return df

    def plot_datasets(self, df_forecast):
        y = go.Scatter(x=self.df['ds'],
                       y=self.df['y'],
                       name='y',
                       line=dict(color='#94B7F5'))
        yhat = go.Scatter(x=df_forecast['ds'],
                          y=df_forecast['yhat'], name='yhat')
        yhat_upper = go.Scatter(x=df_forecast['ds'],
                                y=df_forecast['yhat_upper'],
                                fill='tonexty',
                                mode='none',
                                name='yhat_upper',
                                fillcolor='rgba(0,201,253,.21)')
        yhat_lower = go.Scatter(x=df_forecast['ds'],
                                y=df_forecast['yhat_lower'],
                                fill='tonexty',
                                mode='none',
                                name='yhat_lower',
                                fillcolor='rgba(252,201,5,.05)')
        layout = go.Layout(plot_bgcolor='#2d2929',
                           paper_bgcolor='#2d2929',
                           title='{} Price Forecast'.format(
                               self.from_symbol),
                           font=dict(color='rgb(255, 255, 255)', size=17),
                           legend=dict(orientation="h"),
                           yaxis=dict(
                               side='right',
                               title='Price ({})'.format(self.to_symbol)),
                           xaxis=dict(title=''))
        return offline.plot({'data': [y, yhat, yhat_lower, yhat_upper], 'layout': layout},
                            filename='Nostradamus-prophecy.html')
