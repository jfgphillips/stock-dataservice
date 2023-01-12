import pandas as pd
from pandas import DataFrame



def get_portfolio_stocks_datastore() -> DataFrame:
    data = pd.read_csv("relational_database/portfolio_data.csv")
    data["purchase_date"] = pd.to_datetime(data["purchase_date"], format="%d/%m/%Y %H:%M")
    return data

def get_user_portfolio_datastore() -> DataFrame:
    data = pd.read_csv("relational_database/user_portfolios.csv")
    return data


portfolio_datastore = get_portfolio_stocks_datastore()

user_portfolios_datastore = get_user_portfolio_datastore()


def get_portfolio_stocks(portfolio_id: int) -> DataFrame:
    portfolio = portfolio_datastore[portfolio_datastore['portfolio_id'] == portfolio_id]
    return portfolio


def get_user_portfolios(user_id: int) -> list:
    user_portfolios = user_portfolios_datastore[user_portfolios_datastore["user_id"] == user_id]
    portfolio_list = user_portfolios.portfolio_id.tolist()
    return portfolio_list
