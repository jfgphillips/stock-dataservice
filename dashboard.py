from calculation_engine import calculate_portfolio
from portfolio_data import get_user_portfolio
from fastapi import FastAPI

app = FastAPI()


@app.get("/get_portfolio_by_id")
async def global_method(portfolio_id: int):
    user_portfolio = get_user_portfolio(portfolio_id)
    result = calculate_portfolio(user_portfolio)
    return result

