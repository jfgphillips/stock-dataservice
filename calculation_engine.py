from datetime import datetime
import yfinance as yf
from pandas import DataFrame
from typing import Union
import plotly.express as px
from flask import render_template



yf.pdr_override()


def get_raw_data_by_ticker(ticker: str, start: str, end: Union[str, datetime]) -> DataFrame:
    data = yf.download(ticker, start=start, end=end, interval="1m")
    return data


def get_net_gain(stock_data: DataFrame, units: int) -> int:
    return (stock_data["Open"][0] - stock_data["Close"][-1]) * units

def generate_pie_chart(df, metric):
    current_value = df["purchase_units"] * df[metric]
    fig = px.pie(df, values=current_value, names='stock_ticker')
    return fig


def calculate_portfolio(data: DataFrame):
    date_today = datetime.now()
    for index, stock in data.iterrows():
        print(stock["stock_ticker"])
        return_data = get_raw_data_by_ticker(ticker=stock["stock_ticker"], start=stock["purchase_date"], end=date_today)
        if not return_data.empty:
            data.loc[index, "purchase_price"] = return_data["Open"][0]
            data.loc[index, "current_price"] = return_data["Close"][-1]
            data.loc[index, "net_gain"] = get_net_gain(return_data, units=stock["purchase_units"])
            data.loc[index, "current_date"] = date_today
    pie_chart = generate_pie_chart(data, "current_price")
    pie_chart.write_html("templates/current_price.html")
    return render_template('templates/current_price.html')
