import os
from calculation_engine import calculate_portfolio
from portfolio_data import get_user_portfolio
from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome_page():
    page_welcome = "Welcome to MegaCorp's Portfolio Website"
    return page_welcome



@app.get("/get_portfolio_by_id")
async def global_method(portfolio_id: int):
    user_portfolio = get_user_portfolio(portfolio_id)
    result = calculate_portfolio(user_portfolio)
    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

