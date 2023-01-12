import pandas as pd
from pandas import DataFrame


def get_portfolio_datastore() -> DataFrame:
    data = pd.read_csv("portfolio_data.csv")
    data["purchase_date"] = pd.to_datetime(data["purchase_date"], format="%d/%m/%Y %H:%M")
    return data


portfolio_datastore = get_portfolio_datastore()


def get_user_portfolio(portfolio_id: int) -> DataFrame:
    portfolio = portfolio_datastore[portfolio_datastore['portfolio_id'] == portfolio_id]
    return portfolio
